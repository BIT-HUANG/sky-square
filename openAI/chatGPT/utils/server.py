import openai
openai.api_key='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'

# 系统信息（system）：用于设定助手的表现。
# 助手信息（assistant）：助手回复的信息。（用于多轮对话）
# 用户信息（user）：用户的聊天、问题信息。

total_tokens=0
messages=[]
messages.append({"role":"system","content":'你现在是很有用的助手！ '})

while 1:
    cnt=int((len(messages)-1)/2) #大致估计对答次数
    if cnt >= 2:
        print("GPT已经回答了" + str(cnt) + "个问题了，目前当次提问成本是"+
              str(total_tokens)+"tokens,您可以\n1.输入init重置上下文历史减少tokens使用\n2.输入exit结束对话\n3.钱多任性继续提问")
    message = input("用户提问: \n")
    if message == "exit":
        print("对话结束，山水有相逢")
        break
    #由于对话会保留大量上下文，一般建议对答5轮就要考虑清掉上下文重新讨论
    if message == "init":
        messages = []
        messages.append({"role": "system", "content": '你现在是很有用的助手！ '})
        print("上下文重置，请重新提问。")
        continue

    messages.append({"role":"user","content":message})
    response=openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        #model可选"gpt-3.5-turbo"与"gpt-3.5-turbo-0301","text-davinci-003"
        messages=messages)

    total_tokens=response['usage']['total_tokens']
    reply = response['choices'][0]['message']['content'].strip().encode('utf-8').decode()
    messages.append({"role":"assistant","content":reply})

    print("\n"+ "GPT回答: \n",reply+'\n')