/**
 * RAW AI - Integração Frontend com Backend Python
 */

const RAW_AI_ENGINE = {
    backendUrl: 'muriloagliardi-production.up.railway.app',

    // Captura todo o estado da sessão no site
    getCurrentSiteContext() {
        // Pega o produto atual se estiver na página de produto
        let currentProduct = null;
        const urlParams = new URLSearchParams(window.location.search);
        const prodId = urlParams.get('id');

        if (prodId && typeof PRODUCTS_DB !== 'undefined') {
            currentProduct = PRODUCTS_DB.find(p => p.id === prodId) || null;
        }

        // Pega os produtos do catálogo dinâmico
        const catalog = typeof getStoreProducts === 'function' ? getStoreProducts() : (typeof PRODUCTS_DB !== 'undefined' ? PRODUCTS_DB : []);

        return {
            current_page: window.location.pathname.split('/').pop() || 'index.html',
            current_product: currentProduct,
            cart_items: AppState.cart || [],
            catalog: catalog
        };
    },

    // Envia mensagem do usuário + Contexto para o Servidor Python
    async sendMessage(userMessage) {
        const siteContext = this.getCurrentSiteContext();

        try {
            const response = await fetch(this.backendUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_message: userMessage,
                    current_page: siteContext.current_page,
                    current_product: siteContext.current_product,
                    cart_items: siteContext.cart_items,
                    catalog: siteContext.catalog
                })
            });

            if (!response.ok) {
                throw new Error('Falha de comunicação com a IA Python.');
            }

            const data = await response.json();
            return data.reply;

        } catch (error) {
            console.error('Erro na IA:', error);
            return 'Ops, tive um problema ao me conectar com o servidor Python. Verifique se o backend está rodando!';
        }
    }
};
