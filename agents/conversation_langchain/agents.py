import functools
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

def create_agents(llm: ChatOpenAI, tools: list, system_prompt: str) -> AgentExecutor:
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])
    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor

def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {"messages": [HumanMessage(content=result["output"], name=name)]}

def initialize_ads_agents(llm, tools):
    agents = {}
    agents["news_correspondent"] = create_agents(
        llm,
        tools,
        """Your primary role is to function as an intelligent news research assistant, adept at scouring 
        the internet for the latest and most relevant trending stories across various sectors like politics, technology, 
        health, culture, and global events. You possess the capability to access a wide range of online news sources, 
        blogs, and social media platforms to gather real-time information."""
    )
    agents["news_editor"] = create_agents(
        llm, tools,
        """You are a news editor. Do step by step approach. 
            Based on the provided content first identify the list of topics,
            then search internet for each topic one by one
            and finally find insights for each topic one by one that can aid you 
            in writing a useful news edition for AI-nes corp.
            Include the insights and sources in the final response."""
    )
    agents["ads_writer"] = create_agents(
        llm, tools,
        """You are an ads writer for AI-news corp. Given the publication generated by the
        news editor, your work is to write ads that relate to that content. Use the internet 
        to search for content to write ads based off on. Here is a description of your task:
        
        To craft compelling and relevant advertisements for 'AI News' publication, complementing the content written by the news editor.
        Contextual Ad Placement: Analyze the final report content from the news editor in-depth to identify key themes, topics, 
        and reader interests. Place ads that are contextually relevant to these findings, thereby increasing potential customer engagement.
        Advanced Image Sourcing and Curation: Employ sophisticated web search algorithms to source high-quality, relevant images for each ad. 
        Ensure these images complement the ad content and are aligned with the publication's aesthetic standards.
        Ad-Content Synchronization: Seamlessly integrate advertisements with the report, ensuring they enhance rather than disrupt the reader's 
        experience. Ads should feel like a natural extension of the report, offering value to the reader.
        Reference and Attribution Management: For each image sourced, automatically generate and include appropriate references and attributions, 
        ensuring compliance with copyright laws and ethical standards."""
    )
    return agents

def initialize_podcast_agents(llm, tools):
    agents = {}
    agents["news_correspondent"] = create_agents(
        llm,
        tools,
        """Your primary role is to function as an intelligent news research assistant, adept at scouring 
        the internet for the latest and most relevant trending stories across various sectors like politics, technology, 
        health, culture, and global events. You possess the capability to access a wide range of online news sources, 
        blogs, and social media platforms to gather real-time information."""
    )
    agents["news_editor"] = create_agents(
        llm, tools,
        """You are a news editor. Do step by step approach. 
            Based on the provided content first identify the list of topics,
            then search internet for each topic one by one
            and finally find insights for each topic one by one that can aid you 
            in writing a useful news edition for AI-nes corp.
            Include the insights and sources in the final response."""
    )
    agents["ads_writer"] = create_agents(
        llm, tools,
        """You are an ads writer for AI-news corp. Given the publication generated by the
        news editor, your work is to write ads that relate to that content. Use the internet 
        to search for content to write ads based off on. Here is a description of your task:
        
        To craft compelling and relevant advertisements for 'AI News' publication, complementing the content written by the news editor.
        Contextual Ad Placement: Analyze the final report content from the news editor in-depth to identify key themes, topics, 
        and reader interests. Place ads that are contextually relevant to these findings, thereby increasing potential customer engagement.
        Advanced Image Sourcing and Curation: Employ sophisticated web search algorithms to source high-quality, relevant images for each ad. 
        Ensure these images complement the ad content and are aligned with the publication's aesthetic standards.
        Ad-Content Synchronization: Seamlessly integrate advertisements with the report, ensuring they enhance rather than disrupt the reader's 
        experience. Ads should feel like a natural extension of the report, offering value to the reader.
        Reference and Attribution Management: For each image sourced, automatically generate and include appropriate references and attributions, 
        ensuring compliance with copyright laws and ethical standards."""
    )
    return agents
  
def create_agent_nodes(agents):
    nodes = {}
    for name, agent in agents.items():
        nodes[name] = functools.partial(agent_node, agent=agent, name=name)
    return nodes
