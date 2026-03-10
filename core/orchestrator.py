from typing import Dict, Any

from core.state_manager import ProjectState
from agents.planning_agent import PlanningAgent
from agents.development_agent import DevelopmentAgent
from agents.testing_agent import TestingAgent
from agents.delivery_agent import DeliveryAgent
from core.logger import get_logger


logger = get_logger(__name__)


class Orchestrator:
    def __init__(self, initial_state: Dict[str, Any] = None):
        self.state = ProjectState(initial_state or {}).data

    def run(self) -> Dict[str, Any]:
        logger.info("Starting orchestration")
        try:
            for agent_cls in [PlanningAgent, DevelopmentAgent, TestingAgent, DeliveryAgent]:
                agent = agent_cls(self.state)
                logger.info(f"Running {agent_cls.__name__}")
                self.state = agent.run()
                logger.info(f"State after {agent_cls.__name__}: {self.state}")
        except Exception as e:
            logger.error(f"Orchestration failed: {e}")
            raise
        logger.info("Orchestration complete")
        return self.state
