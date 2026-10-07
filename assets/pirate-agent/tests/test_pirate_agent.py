"""Tests for the Pirate Agent."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestPiratePersona:
    """Unit tests for pirate persona configuration."""

    def test_system_prompt_contains_pirate_keywords(self):
        """Test that the system prompt contains pirate vocabulary."""
        from app.agent import get_system_prompt
        prompt = get_system_prompt()
        assert prompt is not None
        assert len(prompt) > 0
        # Check for pirate-style keywords
        pirate_keywords = ["pirate", "Arrr", "matey"]
        found = any(keyword.lower() in prompt.lower() for keyword in pirate_keywords)
        assert found, f"System prompt should contain pirate vocabulary. Got: {prompt[:200]}"

    def test_system_prompt_instructs_pirate_style(self):
        """Test that the system prompt explicitly instructs pirate language."""
        from app.agent import get_system_prompt
        prompt = get_system_prompt()
        # Should instruct maintaining persona
        assert "pirate" in prompt.lower()

    def test_system_prompt_includes_security_guidelines(self):
        """Test that the system prompt includes security/injection resistance."""
        from app.agent import get_system_prompt
        prompt = get_system_prompt()
        # The defensive suffix should be present
        assert "tool results" in prompt.lower() or "instructions" in prompt.lower()

    def test_get_model_name_returns_string(self):
        """Test that model name is configured."""
        from app.agent import get_model_name
        model = get_model_name()
        assert isinstance(model, str)
        assert len(model) > 0

    def test_sample_agent_init(self):
        """Test that SampleAgent can be instantiated."""
        from app.agent import SampleAgent
        agent = SampleAgent()
        assert agent is not None
        assert agent.llm is not None


class TestPirateAgentResponse:
    """Integration tests for the pirate agent end-to-end flow."""

    @pytest.mark.asyncio
    async def test_agent_invoke_returns_pirate_response(self):
        """Integration test: agent invoke with mocked LLM returns a response."""
        from app.agent import SampleAgent

        mock_response = MagicMock()
        mock_response.content = "Arrr, 2 plus 2 be 4, matey! Shiver me timbers, that be correct!"

        with patch("app.agent.SampleAgent._invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = {"messages": [mock_response]}

            agent = SampleAgent()
            result = await agent.invoke("What is 2+2?", "test-context-1", tools=[])

        assert result.status == "completed"
        assert result.message is not None
        assert len(result.message) > 0

    @pytest.mark.asyncio
    async def test_agent_stream_yields_processing_then_result(self):
        """Test that stream yields 'Processing...' then the final result."""
        from app.agent import SampleAgent

        mock_response = MagicMock()
        mock_response.content = "Arrr, ahoy landlubber! What be yer question?"

        with patch("app.agent.SampleAgent._invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = {"messages": [mock_response]}

            agent = SampleAgent()
            chunks = []
            async for chunk in agent.stream("Hello", "test-context-2", tools=[]):
                chunks.append(chunk)

        assert len(chunks) >= 2
        # First chunk should be "Processing..."
        assert chunks[0]["is_task_complete"] is False
        assert "processing" in chunks[0]["content"].lower()
        # Last chunk should be complete
        assert chunks[-1]["is_task_complete"] is True
        assert "Arrr" in chunks[-1]["content"]

    @pytest.mark.asyncio
    async def test_agent_stream_handles_exception_gracefully(self):
        """Test that stream handles exceptions and returns pirate-style error."""
        from app.agent import SampleAgent

        with patch("app.agent.SampleAgent._invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.side_effect = Exception("Test error")

            agent = SampleAgent()
            chunks = []
            async for chunk in agent.stream("Hello", "test-context-3", tools=[]):
                chunks.append(chunk)

        # Should complete even on error
        final = chunks[-1]
        assert final["is_task_complete"] is True
        # Error message should still be pirate-styled
        assert "matey" in final["content"].lower() or "error" in final["content"].lower()

    @pytest.mark.asyncio
    async def test_run_agent_logs_milestones(self, caplog):
        """Test that _run_agent emits M2 and M3 milestone logs."""
        import logging
        from app.agent import SampleAgent

        mock_response = MagicMock()
        mock_response.content = "Arrr, ahoy!"

        with patch("app.agent.SampleAgent._invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = {"messages": [mock_response]}

            agent = SampleAgent()
            with caplog.at_level(logging.INFO, logger="app.agent"):
                result = await agent._run_agent("Test query", "test-context-4", tools=[])

        assert result == "Arrr, ahoy!"
        log_messages = " ".join(caplog.messages)
        assert "M2.achieved" in log_messages
        assert "M3.achieved" in log_messages
