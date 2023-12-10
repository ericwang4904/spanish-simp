from model import LS
from prompts import *
from request_handler import rawtext_from_url


url = 'https://www.cnn.com/2023/12/09/weather/montgomery-county-tennessee-tornado-fatalities/index.html'
rawtext = rawtext_from_url(url)

#user = "An English professor with a PhD in linguistics who has expert knowlege on all subjects"
user = "A foreign English speaking high school who is able to read simple text but struggles with harder sentences"
#user = "An English beginner who is unfamiliar with reading english news reporting"

a=LS(user=user, text=rawtext, language='English')

lb = 19
ub = lb + 4

response = a.cwi(lb, ub)

for i in range(lb, ub):
    print("-" * 10)
    print(f"Sentence: {a.sentences[i]}")
    print(f"Complex: {response['completion'][i - lb]}")




