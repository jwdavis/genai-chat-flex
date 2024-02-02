import streamlit as st
import asyncio
from langchain_openai import OpenAI

st.set_page_config(
    page_title='ROI GenAI Chat',
    page_icon='./static/ROISquareLogo.png',
)


async def func1(prompt, container):
    container.write("Function is running")
    prompt = f"""
    You are a helpful assistant. Please keep your answers brief, under 300 
    words. Please respond to the following prompt:

    {prompt}
    """
    chat = OpenAI(
        openai_api_key="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",
        model="gpt-3.5-turbo-instruct"
    )
    response = await chat.ainvoke(prompt)
    for i in range(3):
        container.write(i)
        await asyncio.sleep(1)
    container.write(response)
    return response


async def func2(prompt, container):
    container.write("Function 2 is running")
    prompt = f"""
    You are a helpful assistant. Please keep your answers brief, under 300 
    words. Please respond to the following prompt:

    {prompt}
    """
    chat = OpenAI(
        openai_api_key="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",
        model="gpt-3.5-turbo-instruct"
    )
    response = await chat.ainvoke(prompt)
    for i in range(3):
        container.write(i)
        await asyncio.sleep(1)
    container.write(response)
    return response


async def main():
    col1, col2 = st.columns(2)
    with col1:
        t1c = st.empty()
    prompt = "tell me about the earth"
    t1 = asyncio.create_task(func1(prompt, t1c))
    prompt = "tell me about the sun"
    with col2:
        t2c = st.empty()
    t2 = asyncio.create_task(func2(prompt, t2c))

    await t1
    await t2

    st.write("Both functions have completed")

if __name__ == "__main__":
    asyncio.run(main())
