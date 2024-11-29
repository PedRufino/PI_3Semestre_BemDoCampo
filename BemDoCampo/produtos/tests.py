# test.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Produtos
import uuid

User = get_user_model()

class ProductsViewTest(TestCase):
    def setUp(self):
        # Configura o cliente e cria um usuário de teste com email
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='12345')
        self.client.login(email='testuser@example.com', password='12345')
        
        # Dados do produto para os testes
        self.product_data = {
            'nome': 'Melancia',
            'tipo_produto': 'fruta',
            'quantidade': 10,
            'tipo_unidade': 'kg',
            'valor': 24.99,
            'descricao': 'Melancia doce e fresca'
        }

        # Cria um produto inicial para testes de edição e exclusão
        self.produto = Produtos.objects.create(
            produto_id=str(uuid.uuid4()),
            produtor_id=self.user.id,
            **self.product_data
        )

    def test_get_products_view(self):
        # Testa se a página de produtos carrega corretamente com o formulário em branco
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products.html')
        self.assertIn('form', response.context)

    def test_get_product_edit_view(self):
        # Testa se a página de edição carrega o produto existente
        response = self.client.get(reverse('edit_product', kwargs={'produto_id': str(self.produto.produto_id)}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.produto.nome)
        self.assertContains(response, self.produto.valor)

    def test_post_create_product(self):
        # Testa a criação de um novo produto via POST
        response = self.client.post(reverse('products'), {
            'produto_id': '',
            'produtor_id':self.user.id,
            'nome': 'Abacaxi',
            'tipo_produto': 'fruta',
            'quantidade': 5,
            'tipo_unidade': 'un',
            'valor': 15.00,
            'descricao': 'Abacaxi doce'
        })
        
        self.assertEqual(response.status_code, 302)  # Redireciona após criação
        self.assertTrue(Produtos.objects.filter(nome='Abacaxi').count() > 0)

    def test_post_update_product(self):
        # Testa a atualização de um produto existente via POST
        response = self.client.post(reverse('products'), {
            'produto_id': self.produto.produto_id,
            'produtor_id':self.user.id,
            'nome': 'Melancia Atualizada',
            'tipo_produto': 'fruta',
            'quantidade': 20,
            'tipo_unidade': 'kg',
            'valor': 30.00,
            'descricao': 'Melancia mais doce'
        })
        self.assertEqual(response.status_code, 302)  # Redireciona após atualização
        response = self.client.get(reverse('stock'))
        self.assertContains(response, 'Melancia Atualizada')
        self.assertContains(response, '20')

    def test_delete_product(self):
        # Testa a exclusão de um produto existente
        response = self.client.get(reverse('delete_product', kwargs={'produto_id': self.produto.produto_id}))
        self.assertEqual(response.status_code, 302)  # Redireciona após exclusão
        self.assertFalse(Produtos.objects.filter(produto_id=self.produto.produto_id))

class StockViewTest(TestCase):
    def setUp(self):
        # Configura o cliente e cria um usuário de teste com email
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='12345')
        self.client.login(email='testuser@example.com', password='12345')
        
        # Cria alguns produtos para o usuário
        for i in range(3):
            Produtos.objects.create(
                produto_id=str(uuid.uuid4()),
                produtor_id=self.user.id,
                nome=f'Produto {i}',
                tipo_produto='fruta',
                quantidade=10,
                tipo_unidade='kg',
                valor=10.00,
                descricao=f'Descrição do produto {i}'
            )

    def test_get_stock_view(self):
        # Testa se a página de estoque carrega corretamente com todos os produtos do usuário
        response = self.client.get(reverse('stock'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stock.html')
        self.assertTrue(len(response.context['produtos']) > 0) # Verifica se existe itens no estoque
