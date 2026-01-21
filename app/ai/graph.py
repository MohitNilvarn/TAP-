# File: app/ai/graph.py
"""
LangGraph workflow for content generation.

This module implements a state machine using LangGraph that:
1. Retrieves relevant context from the vector store
2. Generates notes based on transcript + context
3. Generates assignments based on transcript + context
4. Generates flashcards based on transcript + context
5. Saves all generated content to MongoDB
"""
from typing import TypedDict, Optional, List, Dict, Any
from datetime import datetime
from langgraph.graph import StateGraph, END
from beanie import PydanticObjectId

from app.core.logger import get_logger
from app.services.vector_store import search_documents
from app.ai.llm import generate_json
from app.ai.prompts import (
    SYSTEM_PROMPT,
    get_notes_prompt,
    get_assignment_prompt,
    get_flashcards_prompt
)
from app.models.content import GeneratedContent, ContentType
from app.models.lecture import Lecture, GenerationStatus

logger = get_logger("TAP.AIGraph")


# Define the state schema
class ContentGenerationState(TypedDict):
    """State for content generation workflow."""
    # Input
    lecture_id: str
    course_id: str
    transcript: str
    lecture_title: str
    content_types: List[str]  # Which types to generate
    
    # Retrieved context
    context: str
    context_documents: List[Dict[str, Any]]
    
    # Generated content
    notes: Optional[Dict[str, Any]]
    assignment: Optional[Dict[str, Any]]
    flashcards: Optional[Dict[str, Any]]
    
    # Status
    error: Optional[str]
    completed_types: List[str]


async def retrieve_context_node(state: ContentGenerationState) -> ContentGenerationState:
    """
    Node: Retrieve relevant context from vector store.
    """
    logger.info(f"Retrieving context for lecture: {state['lecture_id']}")
    
    try:
        # Search for relevant documents using the transcript as query
        # Use first 500 chars of transcript as search query
        query = state["transcript"][:500] if state["transcript"] else state["lecture_title"]
        
        results = search_documents(
            course_id=state["course_id"],
            query=query,
            n_results=5
        )
        
        # Combine context from search results
        context_parts = []
        for result in results:
            if result.get("document"):
                context_parts.append(result["document"])
        
        context = "\n\n---\n\n".join(context_parts) if context_parts else "No additional context available."
        
        logger.info(f"Retrieved {len(results)} context documents")
        
        return {
            **state,
            "context": context,
            "context_documents": results
        }
    except Exception as e:
        logger.error(f"Context retrieval error: {str(e)}")
        return {
            **state,
            "context": "No additional context available.",
            "context_documents": []
        }


async def generate_notes_node(state: ContentGenerationState) -> ContentGenerationState:
    """
    Node: Generate lecture notes.
    """
    if "notes" not in state["content_types"]:
        logger.info("Skipping notes generation (not requested)")
        return state
    
    logger.info(f"Generating notes for lecture: {state['lecture_id']}")
    
    try:
        prompt = get_notes_prompt(
            transcript=state["transcript"],
            context=state["context"],
            lecture_title=state["lecture_title"]
        )
        
        notes = await generate_json(prompt, SYSTEM_PROMPT)
        
        logger.info("Notes generated successfully")
        
        completed = state.get("completed_types", [])
        completed.append("notes")
        
        return {
            **state,
            "notes": notes,
            "completed_types": completed
        }
    except Exception as e:
        logger.error(f"Notes generation error: {str(e)}")
        return {
            **state,
            "error": f"Notes generation failed: {str(e)}"
        }


async def generate_assignment_node(state: ContentGenerationState) -> ContentGenerationState:
    """
    Node: Generate practice assignment.
    """
    if "assignment" not in state["content_types"]:
        logger.info("Skipping assignment generation (not requested)")
        return state
    
    logger.info(f"Generating assignment for lecture: {state['lecture_id']}")
    
    try:
        prompt = get_assignment_prompt(
            transcript=state["transcript"],
            context=state["context"],
            lecture_title=state["lecture_title"]
        )
        
        assignment = await generate_json(prompt, SYSTEM_PROMPT)
        
        logger.info("Assignment generated successfully")
        
        completed = state.get("completed_types", [])
        completed.append("assignment")
        
        return {
            **state,
            "assignment": assignment,
            "completed_types": completed
        }
    except Exception as e:
        logger.error(f"Assignment generation error: {str(e)}")
        return {
            **state,
            "error": f"Assignment generation failed: {str(e)}"
        }


async def generate_flashcards_node(state: ContentGenerationState) -> ContentGenerationState:
    """
    Node: Generate flashcards.
    """
    if "flashcards" not in state["content_types"]:
        logger.info("Skipping flashcards generation (not requested)")
        return state
    
    logger.info(f"Generating flashcards for lecture: {state['lecture_id']}")
    
    try:
        prompt = get_flashcards_prompt(
            transcript=state["transcript"],
            context=state["context"],
            lecture_title=state["lecture_title"]
        )
        
        flashcards = await generate_json(prompt, SYSTEM_PROMPT)
        
        logger.info("Flashcards generated successfully")
        
        completed = state.get("completed_types", [])
        completed.append("flashcards")
        
        return {
            **state,
            "flashcards": flashcards,
            "completed_types": completed
        }
    except Exception as e:
        logger.error(f"Flashcards generation error: {str(e)}")
        return {
            **state,
            "error": f"Flashcards generation failed: {str(e)}"
        }


async def save_content_node(state: ContentGenerationState) -> ContentGenerationState:
    """
    Node: Save generated content to MongoDB.
    """
    logger.info(f"Saving generated content for lecture: {state['lecture_id']}")
    
    try:
        saved_count = 0
        
        # Save notes
        if state.get("notes"):
            notes_doc = GeneratedContent(
                lecture_id=state["lecture_id"],
                course_id=state["course_id"],
                content_type=ContentType.NOTES,
                content=state["notes"],
                metadata={
                    "context_docs_used": len(state.get("context_documents", [])),
                    "generated_at": datetime.utcnow().isoformat()
                }
            )
            await notes_doc.insert()
            saved_count += 1
            logger.info("Notes saved to database")
        
        # Save assignment
        if state.get("assignment"):
            assignment_doc = GeneratedContent(
                lecture_id=state["lecture_id"],
                course_id=state["course_id"],
                content_type=ContentType.ASSIGNMENT,
                content=state["assignment"],
                metadata={
                    "context_docs_used": len(state.get("context_documents", [])),
                    "generated_at": datetime.utcnow().isoformat()
                }
            )
            await assignment_doc.insert()
            saved_count += 1
            logger.info("Assignment saved to database")
        
        # Save flashcards
        if state.get("flashcards"):
            flashcards_doc = GeneratedContent(
                lecture_id=state["lecture_id"],
                course_id=state["course_id"],
                content_type=ContentType.FLASHCARDS,
                content=state["flashcards"],
                metadata={
                    "context_docs_used": len(state.get("context_documents", [])),
                    "generated_at": datetime.utcnow().isoformat()
                }
            )
            await flashcards_doc.insert()
            saved_count += 1
            logger.info("Flashcards saved to database")
        
        # Update lecture status
        lecture = await Lecture.get(state["lecture_id"])
        if lecture:
            lecture.generation_status = GenerationStatus.COMPLETED
            lecture.generated_at = datetime.utcnow()
            await lecture.save()
        
        logger.info(f"Saved {saved_count} content items")
        
        return state
        
    except Exception as e:
        logger.error(f"Content save error: {str(e)}")
        return {
            **state,
            "error": f"Failed to save content: {str(e)}"
        }


def build_content_generation_graph() -> StateGraph:
    """
    Build the LangGraph workflow for content generation.
    
    Flow:
    1. retrieve_context -> 2. generate_notes -> 3. generate_assignment
    -> 4. generate_flashcards -> 5. save_content -> END
    """
    workflow = StateGraph(ContentGenerationState)
    
    # Add nodes
    workflow.add_node("retrieve_context", retrieve_context_node)
    workflow.add_node("generate_notes", generate_notes_node)
    workflow.add_node("generate_assignment", generate_assignment_node)
    workflow.add_node("generate_flashcards", generate_flashcards_node)
    workflow.add_node("save_content", save_content_node)
    
    # Define edges (sequential flow)
    workflow.set_entry_point("retrieve_context")
    workflow.add_edge("retrieve_context", "generate_notes")
    workflow.add_edge("generate_notes", "generate_assignment")
    workflow.add_edge("generate_assignment", "generate_flashcards")
    workflow.add_edge("generate_flashcards", "save_content")
    workflow.add_edge("save_content", END)
    
    return workflow.compile()


# Compiled workflow instance
content_generation_graph = build_content_generation_graph()


async def run_content_generation(
    lecture_id: str,
    course_id: str,
    transcript: str,
    lecture_title: str,
    content_types: List[str] = None
) -> Dict[str, Any]:
    """
    Run the content generation workflow.
    
    Args:
        lecture_id: ID of the lecture
        course_id: ID of the course
        transcript: Lecture transcript text
        lecture_title: Title of the lecture
        content_types: List of content types to generate
    
    Returns:
        Final state with generated content
    """
    if content_types is None:
        content_types = ["notes", "assignment", "flashcards"]
    
    initial_state: ContentGenerationState = {
        "lecture_id": lecture_id,
        "course_id": course_id,
        "transcript": transcript,
        "lecture_title": lecture_title,
        "content_types": content_types,
        "context": "",
        "context_documents": [],
        "notes": None,
        "assignment": None,
        "flashcards": None,
        "error": None,
        "completed_types": []
    }
    
    logger.info(f"Starting content generation workflow for lecture: {lecture_id}")
    
    # Run the workflow
    final_state = await content_generation_graph.ainvoke(initial_state)
    
    logger.info(f"Content generation complete. Types: {final_state.get('completed_types', [])}")
    
    return final_state
