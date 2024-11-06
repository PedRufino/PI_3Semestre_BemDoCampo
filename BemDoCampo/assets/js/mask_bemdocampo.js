function mask_document(id) {
    $(document).ready(function(){
        var documentInput = $(id);
    
        documentInput.on('input', function() {
            this.value = this.value.replace(/\D/g, '');
        });
    
        documentInput.on('focus', function() {
            $(this).unmask();
        });
    
        documentInput.on('blur', function() {
            var val = $(this).val();
    
            if (val.length > 11) {
                $(this).mask('00.000.000/0000-00', {reverse: true});
            } 
            else if (val.length === 11) {
                $(this).mask('000.000.000-00', {reverse: true});
            }
        });
    });
}

function mask_contato(id) {
    $(document).ready(function() {
        var documentInput = $(id);
    
        documentInput.on('input', function() {
            this.value = this.value.replace(/\D/g, '');
        });
    
        documentInput.on('focus', function() {
            $(this).unmask();
        });
    
        documentInput.on('blur', function() {
            var val = $(this).val();
    
            if (val.length === 11) {
                $(this).mask('(00) 00000-0000');
            } 
            else if (val.length === 10) {
                $(this).mask('(00) 0000-0000');
            }
        });
    });
}

function mask_date(id) {
    $(document).ready(function(){
        var documentInput = $(id);
        
        documentInput.on('input', function() {
            var val = $(this).val().replace(/\D/g, '');
            $(this).mask('00/00/0000');
        });
    });
}

function mask_validity(id) {
    $(document).ready(function(){
        var documentInput = $(id);
        
        documentInput.on('input', function() {
            var val = $(this).val().replace(/\D/g, '');
            $(this).mask('00/00');
        });
    });
}

function mask_numberCard(id) {
    $(document).ready(function(){
        var documentInput = $(id);
        
        documentInput.on('input', function() {
            var val = $(this).val().replace(/\D/g, '');
            $(this).mask('0000 0000 0000 0000');
        });
    });
}

function mask_money(id) {
    $(document).ready(function(){
        var documentInput = $(id);
        
        documentInput.on('input', function() {
            var val = $(this).val().replace(/\D/g, '');
            $(this).mask('000.000.000.000.000,00', {reverse: true});
        });

        $('form').on('submit', function() {
            var cleanValue = documentInput.val().replace(/\D/g, ''); // Limpa a máscara
            documentInput.val((cleanValue.slice(0, -2) + '.' + cleanValue.slice(-2))); // Formata o valor para decimal
        });
    });
}

function mask_cep(id) {
    $(document).ready(function(){
        var documentInput = $(id);
        
        documentInput.on('input', function() {
            var val = $(this).val().replace(/\D/g, '');
            $(this).mask('00000-000');
        });
    });
}

function busca_cep(id) {
    $(document).ready(function() {
        $(id).on('input', async function() {
            const cep = $(this).val();

            // Limpa os valores anteriores
            $('#logradouro-input').val('');
            $('#bairro-input').val('');
            $('#cidade-input').val('');
            $('#estado-input').val('');

            // Verifica se o CEP é válido
            if (!/^\d{5}-?\d{3}$/.test(cep)) {
                return; // Não faz nada se o CEP não for válido
            }

            // Faz a requisição para a API do ViaCEP
            try {
                const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
                const data = await response.json();

                // Verifica se o CEP retornou resultados
                if (data.erro) {
                    // Crie um elemento div para o alerta
                    const alertDiv = document.createElement('div');
                    alertDiv.className = 'alert alert-danger alert-dismissible fade show mt-2';
                    alertDiv.role = 'alert';

                    // Adicione o ícone e o texto do alerta
                    alertDiv.innerHTML = `
                        <span class="alert-icon"><i class="ni ni-like-2"></i></span>
                        <span class="alert-text"><strong>CEP</strong> não foi encontrado</span>
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    `;

                    // Estilize o alerta para aparecer no topo
                    alertDiv.style.position = 'fixed';
                    alertDiv.style.top = '0';
                    alertDiv.style.left = '50%';
                    alertDiv.style.transform = 'translateX(-50%)';
                    alertDiv.style.zIndex = '9999'; // Para garantir que esteja acima de outros elementos

                    // Adicione o alerta ao corpo do documento
                    document.body.appendChild(alertDiv);
                } else {
                    // Insere os dados nos inputs
                    $('#logradouro-input').val(data.logradouro || '');
                    $('#bairro-input').val(data.bairro || '');
                    $('#cidade-input').val(data.localidade || '');
                    $('#estado-input').val(data.uf || '');
                }
            } catch (error) {
                alert('Erro ao buscar o CEP.');
            }
        });
    });
}