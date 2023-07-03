from products.models import Product, WhatsAppProductInfo
from django.contrib.auth.models import User
from users.models import Company
import requests
import json
import ipdb


def seek_products():
    # Este arquivo é para buscar os produtos, de acordo com os ID's, na API do WhatsApp
    # Sua lista de IDs
    id_list = [5464190076945564,7148054508568726,4559842784120739,4678015725648800,4303079719797118,4742727005847721,4749421438495497,4785115708270517,5059394774173528,4969157259826976,5072268639525331,5101609756622919,5110351115684830,5137621989651690,5159330587418686,7558736214201769,4317646281673903,5114963998525852,4723165281093416,4539249636202021,4891024844327807,4677990068984699,5901928193248103,4695630833823753,4817105875015120,4876764795720159,5458786694205450,5499183396776000,5525984850827462,7053738714666442,6113600305366729,6052667551419924,5900172123410083,5566191506783769,5542557145807856,5215954238416673,5367328766613790,5195176650592110,4907696399291697,6896096763794882,4350689511703886,4381383945299499,7064732476902771,4813672232052588,4096403787125735,4671575796293618,3524715080987156,9063715290320034,3715626628562399,6917545988286629,5982058525195073,6064456316955320,4821012027986923,4842481282441382,5778482522212560,4880345118719083,6011787212167503,7441759165849532,4849172885125605,5737254819644646,5267804619998412,6160558650624266,4619141371472221,4788640927919863,5089143394430805,6281211445224361,5846842302078905,5937019619678960,6217013221684332,6252471888096693,4913573032035562,4868029916621345,4617741495009227,4619310494847061,4641234275972966,4701336343235074,4738909996222286,4785984011463151,5772709119441007,5873237059364908,8258551684162686,8223118634396022,7850176215055201,6362785683753237,5012371928878755,4741420472643166,4288323284604429,4923665654417640,6767592463281945,5610717105616337,4703371306406467,5336319653118879,4756464761134213,5568637053163134,4486971054748211,4761424760621239,4766825330105163,5010838248966359,5337265362954345,5206145422817485,5400550056727043,5023743581020220,4758494787521445,4325841377521205,5048001988566052,4975392342509639,4926125914077487,5100781633267998,4744781502272326,5193629130649524,6824947534213114,4788749734546940,4995420433871561,4764382193689879,5167578396640225,4866751206681514,6406504536044901,5921281554571252,8548832448521342,4930051867101041,4423239411121183,5144370645650502,4497836080325508,4790542087700421,4814232121996625,5162621017125615,5205923959439220,5984006841711776,5964079453602563,5340085042785171,4328048427324007,4701471066605858,4837222033011555,6738843859519602,6885016891540071,6849130835158399,6038440219508065,5766654696730318,5498122290283263,5768371286580311,5162722100419139,8460741390666463,5679140275516115,6035008429875269,5763525870408674,8401221379949087,5786395041449257,4362541060516453,4521726911289610,4885670638151975,5038306689628265,4587572368026914,4634293006606078,4844070359004411,4392781414160464,7685004731572206,5468618109872561,4861561133936124,6320272037988012,4681300961999589,5889916717714477,4830206737000125,5861850647161749,6592323054117419,5495185773828271,8724354360911694,4545743415552269,6081393111893581,5984052924945113,5840400912746433,6191408860903513,5927646907357043,5103684736362989,4824335990937648,4867586069994596,5627470757283063,4599253730203863,9150319298374526,7703972233011543,5145613408816279,6964823480257533,7373572289327066,4780326792078022,4735221073239506,4366042573500274,4755288191266479,6620206244708568,5236260566460829,5041759045860184,7675975602414270,5976433795717427,4761446780577129,5073205599390135,4380074692097956,7867239629960711,4525790447532660,4733515920092742,6922558614456037,9022169211158874,8595585190482817,4818087548234889,7307385125939973,6588717784472381,4513291682108887,5863860020387641,6787995897940208,5944999492184107,4806991449367609,4715930288488312,6274857092574645,6474977599247716,8794137820657706]

    # Dicionário para armazenar os resultados
    results = {}

    # Token de autorização
    auth_token = '$2b$10$bxpyVQpI.kYrZQT8OIz6duU2kzm5aqSDSnjF0X6RoCXw7ikZfPVCa'

    # Iterar sobre a lista de IDs
    for id in id_list:
        try:
            # Construir a URL
            url = f'https://apiwpp.brconnect.click/api/alanmagnatadosqueijos/get-product-by-id?phone=557988656151&id={id}'

            # Definir os cabeçalhos
            headers = {
                'accept': '*/*',
                'Authorization': f'Bearer {auth_token}'
            }

            # Fazer a solicitação GET
            response = requests.get(url, headers=headers)

            # Verificar se a solicitação foi bem-sucedida
            if response.status_code in [200, 201]:
                result = response.json()
                result = {k: v.encode().decode('unicode_escape') if isinstance(v, str) else v for k, v in result.items()}
                results[id] = result
            else:
                print(f'Erro ao buscar o ID {id}: {response.status_code}')
                print(f'Detalhes do erro: {response.text}')
        except Exception as e:
            print(f'Erro ao processar o ID {id}: {str(e)}')

    # Salvar os resultados em um arquivo JSON
    try:
        with open('./products/results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False)
    except Exception as e:
        print(f'Erro ao salvar os resultados em um arquivo JSON: {str(e)}')


def create_products():
    filename = './whatsapp/products/products.json'
    with open(filename) as f:
        products = json.load(f)
    print(products)
    magnata_user = User.objects.get_or_create(username='magnatadosqueijos', password='Buceta50!')
    company = Company.objects.get_or_create(name='Magnata dos Queijos', owner=magnata_user[0])

    for product in products:
        retailer_id = product['retailer_id']
        product_id = product['id']
        price = int(product['price']) / 1000
        product_db = Product.objects.get_or_create(name=product['name'], price=price, description=product['description'], company=company[0])
        
        WhatsAppProductInfo.objects.get_or_create(
            id=product_id,
            name=product['name'], 
            description=product['description'], 
            product=product_db[0], 
            company=company[0], 
            retailer_id=retailer_id,
        )


if __name__ == '__main__':
    # seek_products()
    ...