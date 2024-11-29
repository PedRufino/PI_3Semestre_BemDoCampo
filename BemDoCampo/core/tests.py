from mongoengine.connection import get_db
from django.test import TestCase
from unittest.mock import patch
from django.urls import reverse
from datetime import datetime
import json

class ViewsTest(TestCase):
    def setUp(self):
        self.db = get_db()

        self.db.usuarios.insert_one({
            'user_id': 797979797979797979,
            'nome': 'Orlando',
            'sobrenome': 'Saraiva',
            'email': 'orlandosaraiva@gmail.com',
            'documento': '123.456.789-96',
            'contato': '(19) 96846-2201',
            'data_nascimento': {'$date': '2000-11-19T00:00:00.000Z'},
            'cep': '13615-560',
            'endereco': 'Rua da Fatec',
            'numero': 3215,
            'bairro': 'Bairro da Fatec',
            'cidade': 'Araras',
            'estado': 'SP',
            'imagem_perfil': '/NoPhotoUser.png',
            'tipo_usuario': 'agricultor',
            'formas_pagamento': [],
            'data_cadastro': {'$date': '2024-11-23T11:14:06.196Z'},
            'minha_tenda': {
                'id_tenda': 'a7d57a60-52d8-48b8-91d8-099ff2ce0747',
                'nome_tenda': 'Los Hermanos',
                'email': 'loshermanos@comercial.com',
                'documento': '32.165.498/7888-52',
                'contato': '(19) 3475-2203',
                'cep': '13604-208',
                'endereco': 'Rua Cláudio Pierobon',
                'numero': 208,
                'bairro': 'Jardim Nova Europa',
                'cidade': 'Araras',
                'estado': 'SP',
                'imagem_tenda': 'producers/4/4-a7d57a60-52d8-48b8-91d8-099ff2ce0747-20241123.jpg',
                'tx_entrega': 6.54,
                'tempo_entrega': {'min': 45, 'max': 61},
                'data_cadastro': {'$date': '2024-11-23T12:21:06.040Z'},
                'avaliacoes_estrelas': { '5': 5 },
                'media_avaliacoes': 5
            }
        })
        
        self.db.produtos.insert_one({
            'produto_id': 6565656565656565,
            'nome': 'Produto W',
            'tipo_produto': 'oleo',
            'quantidade': 9,
            'tipo_unidade': 'ml',
            'descricao': 'Descrição sobre produto W com características e benefícios...',
            'produtor_id': 797979797979797979,
            'valor': 10.55,
            'imagem_capa': 'NoPhotoProduct.jpg',
            'total_vendas': 52,
            'data_cadastro': {'$date': datetime.now()},
        })
    
    @patch('core.views.mongoengine.connection.get_db')
    def test_favoritos_view(self, mock_get_db):
        mock_get_db.return_value = self.db

        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)

        self.assertIn('produtos', response.context)
        self.assertGreater(len(response.context['produtos']), 0)

        produto = response.context['produtos'][0]
        
        self.assertEqual(produto['nome'], 'Produto W')
        self.assertEqual(produto['valor'], 10.55)
        self.assertEqual(produto['imagem_capa'], 'NoPhotoProduct.jpg')
        self.assertEqual(produto['user']['tempo_entrega'], '45-61')
        self.assertEqual(produto['user']['media_avaliacoes'], 5)
        self.assertEqual(produto['user']['tx_entrega'], 6.54)
    
    @patch('core.views.mongoengine.connection.get_db')
    def test_tendas_list_view(self, mock_get_db):
        mock_get_db.return_value = self.db

        self.db.usuarios.insert_one({
            'user_id': 5959595959595959,
            'nome': 'João',
            'sobrenome': 'Silva',
            'email': 'joao.silva@gmail.com',
            'documento': '123.456.789-96',
            'contato': '(19) 96846-2201',
            'data_nascimento': {'$date': '1998-11-19T00:00:00.000Z'},
            'cep': '13615-561',
            'endereco': 'Rua da Fatec',
            'numero': 81,
            'bairro': 'Barrio da Fatec',
            'cidade': 'Araras',
            'estado': 'SP',
            'imagem_perfil': '/NoPhotoUser.png',
            'tipo_usuario': 'agricultor',
            'formas_pagamento': [],
            'data_cadastro': {'$date': '2024-11-23T11:14:06.196Z'},
            'minha_tenda': {
                'id_tenda': 'a7d57a60-52d8-48b8-91d8-099ff2ce0749',
                'nome_tenda': 'Mercado Silva',
                'email': 'mercado.silva@comercial.com',
                'documento': '32.165.498/7888-53',
                'contato': '(19) 3475-2203',
                'cep': '13604-208',
                'endereco': 'Rua Cláudio Pierobon',
                'numero': 209,
                'bairro': 'Jardim Nova Europa',
                'cidade': 'Araras',
                'estado': 'SP',
                'imagem_tenda': 'producers/5/5-a7d57a60-52d8-48b8-91d8-099ff2ce0748-20241123.jpg',
                'tx_entrega': 5.99,
                'tempo_entrega': {'min': 30, 'max': 45},
                'data_cadastro': {'$date': '2024-11-23T12:21:06.040Z'},
                'avaliacoes_estrelas': { '4': 3, '5': 2 },
                'media_avaliacoes': 4.5
            }
        })

        response = self.client.get(reverse('load_items', kwargs={'page_number': 1}))

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertFalse(data['erro']) 
        self.assertIn('items', data)
        self.assertGreater(len(data['items']), 0)
        self.assertEqual(data['items'][0]['nome_tenda'], 'Los Hermanos')
    
    @patch('core.views.mongoengine.connection.get_db')
    def test_filtros_tendas(self, mock_get_db):
        mock_get_db.return_value = self.db

        response = self.client.get(reverse('load_items', kwargs={'page_number': 1}), {
            'descAvaliacao': 'true',
            'tempoEntrega': 'true',
            'search': 'Los'
        })

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertFalse(data['erro'])
        self.assertIn('items', data)
        self.assertEqual(data['items'][0]['nome_tenda'], 'Los Hermanos')

    def test_sobre_view(self, ):
        response = self.client.get(reverse('sobre'))

        self.assertEqual(response.status_code, 200)

        self.assertIn('paths', response.context)
        self.assertEqual(response.context['paths'], ['Bem do Campo', 'Sobre Nós'])

    def test_contato_view(self):
        response = self.client.get(reverse('contato'))

        self.assertEqual(response.status_code, 200)

        self.assertIn('paths', response.context)
        self.assertEqual(response.context['paths'], ['Bem do Campo', 'Contato'])

    def tearDown(self):
        self.db.produtos.delete_many({'produtor_id': {'$in': [797979797979797979]}})
        self.db.usuarios.delete_many({'user_id': {'$in': [5959595959595959, 797979797979797979]}})

