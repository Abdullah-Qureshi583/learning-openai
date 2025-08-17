```python
1.The agent just requires the name but don't require the instructions

2.When using the runner as sync so it is necessary to use without in async function otherwise will get an error

3.When using the runner as async so it is necessary to use it in the  async function otherwise will get an error

4.It is necessary to marked the function as tool with decorator

5.audioitransaction api -> use for voice to text conversion ->	/v1/audio/transcriptions

6. Always use run and await when working with asyncronously like use asyncio

7. When working with name and instruction teh name is relative and the instructions are different so the agent works correctly. means It works according to the name

8. If the handoff description are also wrong but the the name is relatable so it still works correctly

9. If the handoff desciption is relatable and even the name is not naem is else so agent will be called as teh relatable description and it works even the instruction are not relatable.

10. handoff withour "s" is used to define and override the specific agent like its name , dexcription etc

11. If the name is changes using handoff withour "s" so the llm will see the new name even use the agent with that name even the detailis not related


```
