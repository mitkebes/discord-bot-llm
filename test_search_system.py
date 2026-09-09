# test_search_system.py
import asyncio
import unittest
import json
from web_search import search_duckduckgo, read_url_jina
from search_agent import run_search_augmented_generation, _parse_search_query, _parse_read_url
import llm_client
from bot import LLMBot, setup, POPULAR_GEMINI_MODELS


class TestSearchUtilities(unittest.IsolatedAsyncioTestCase):

    async def test_duckduckgo_search(self):
        results = await search_duckduckgo("python programming", max_results=3)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        first = results[0]
        self.assertIn("title", first)
        self.assertIn("href", first)
        self.assertIn("body", first)
        self.assertTrue(first["href"].startswith("http"))

    async def test_jina_reader(self):
        url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
        content = await read_url_jina(url, max_chars=500)
        self.assertIsInstance(content, str)
        self.assertGreater(len(content), 0)
        self.assertIn("Python", content)

    def test_parsers(self):
        self.assertEqual(_parse_search_query('SEARCH: "latest AI news"'), "latest AI news")
        self.assertEqual(_parse_search_query("search: quantum computing breakthroughs"), "quantum computing breakthroughs")
        self.assertIsNone(_parse_search_query("NO_SEARCH"))

        self.assertEqual(_parse_read_url("READ: https://example.com/article"), "https://example.com/article")
        self.assertEqual(_parse_read_url('READ: <https://example.com/test>'), "https://example.com/test")


class TestSearchAgent(unittest.IsolatedAsyncioTestCase):

    async def test_agent_no_search_needed(self):
        status_updates = []

        async def mock_status(text: str):
            status_updates.append(text)

        async def mock_llm(prompt: str, system: str, history=None):
            if "AI decision router" in system:
                return "NO_SEARCH"
            return "General answer without search."

        response = await run_search_augmented_generation(
            prompt="Tell me a joke",
            system_prompt="You are a funny assistant.",
            history=[],
            query_llm_fn=mock_llm,
            status_callback=mock_status
        )

        self.assertEqual(response, "General answer without search.")
        self.assertTrue(any("Checking if web search is needed" in s for s in status_updates))
        self.assertTrue(any("Generating response" in s for s in status_updates))
        self.assertFalse(any("Searching the web" in s for s in status_updates))

    async def test_agent_with_search_and_read(self):
        status_updates = []

        async def mock_status(text: str):
            status_updates.append(text)

        call_count = {"count": 0}

        async def mock_llm(prompt: str, system: str, history=None):
            call_count["count"] += 1
            if "AI decision router" in system:
                return "SEARCH: latest python release features"
            elif "research assistant gathering information" in system:
                if call_count["count"] == 2:
                    return "READ: https://en.wikipedia.org/wiki/Python_(programming_language)"
                else:
                    return "READY"
            else:
                self.assertIn("WEB SEARCH RESEARCH", system)
                return "Python latest release information synthesized successfully."

        response = await run_search_augmented_generation(
            prompt="What is new in the latest Python release?",
            system_prompt="You are a helpful assistant.",
            history=[],
            query_llm_fn=mock_llm,
            status_callback=mock_status,
            max_search_steps=3
        )

        self.assertEqual(response, "Python latest release information synthesized successfully.")
        self.assertTrue(any("Searching the web for" in s for s in status_updates))
        self.assertTrue(any("Reading webpage" in s for s in status_updates))
        self.assertTrue(any("Generating final response" in s for s in status_updates))

    async def test_agent_error_propagation(self):
        async def mock_error_llm(prompt: str, system: str, history=None):
            return "⚠️ **Gemini API Error (Rate Limit/Quota)**: 429 ResourceExhausted quota exceeded."

        response = await run_search_augmented_generation(
            prompt="What happened today?",
            system_prompt="You are a helpful assistant.",
            history=[],
            query_llm_fn=mock_error_llm
        )

        self.assertTrue(response.startswith("⚠️ **Gemini API Error"))


class TestBotSetupAndSettings(unittest.IsolatedAsyncioTestCase):

    async def test_bot_initialization_and_settings(self):
        bot = LLMBot()
        self.assertIsNotNone(bot)
        self.assertTrue(hasattr(bot, "grounding_enabled"))
        self.assertTrue(hasattr(bot, "llm_provider"))
        self.assertTrue(hasattr(bot, "gemini_model"))
        self.assertTrue(hasattr(bot, "run_in_background"))
        self.assertTrue(hasattr(bot, "max_history"))

        # Verify settings types
        self.assertIn(bot.llm_provider, ["GEMINI", "LMSTUDIO"])
        self.assertIsInstance(bot.max_history, int)
        self.assertIsInstance(bot.run_in_background, bool)

        await setup(bot)
        commands = {cmd.name: cmd for cmd in bot.tree.get_commands()}
        self.assertIn("grounding", commands)
        self.assertIn("websearch", commands)
        self.assertIn("provider", commands)
        self.assertIn("source", commands)
        self.assertIn("model", commands)
        self.assertIn("help", commands)

        # Check default_permissions on admin commands
        self.assertTrue(commands["provider"].default_permissions.administrator)
        self.assertTrue(commands["source"].default_permissions.administrator)
        self.assertTrue(commands["model"].default_permissions.administrator)

    def test_message_chunking(self):
        long_response = "A" * 4500
        parts = [long_response[i:i+2000] for i in range(0, len(long_response), 2000)]
        self.assertEqual(len(parts), 3)
        self.assertEqual(len(parts[0]), 2000)
        self.assertEqual(len(parts[1]), 2000)
        self.assertEqual(len(parts[2]), 500)


if __name__ == "__main__":
    unittest.main()
