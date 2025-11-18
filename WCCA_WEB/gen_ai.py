def genAi(lis):
    from google import genai
    client = genai.Client(api_key="AIzaSyCTqw15QK2X0g0j6rCf36ODkEtBonc1rBY")
    prmp=f"Considering you are an electrical expert, identify the circuit based on the list of ICs used in it {lis}. Give me a single-line answer."

    response = client.models.generate_content(model="gemini-2.0-flash", contents=prmp)
    #print(response.text)

    raw_text = response.text.replace("**", "")
    
    return raw_text
    