/**
 * RAW AI - Assistente Executivo do Admin
 */

const RAW_ADMIN_AI = {
  backendUrl: 'muriloagliardi-production.up.railway.app',

  // Coleta dados em tempo real da sua dashboard/banco local
  getAdminContext() {
    const catalog = typeof PRODUCTS_DB !== 'undefined' ? PRODUCTS_DB : [];
    const sales = typeof SALES_HISTORY !== 'undefined' ? SALES_HISTORY : [];

    return {
      total_products: catalog.length,
      out_of_stock: catalog.filter(p => p.stock === 0),
      low_stock: catalog.filter(p => p.stock > 0 && p.stock <= 5),
      inventory_summary: catalog.map(p => ({
        id: p.id,
        name: p.name,
        stock: p.stock,
        price: p.price
      })),
      recent_sales: sales
    };
  },

  async askAdminAI(userQuery) {
    const dashboardData = this.getAdminContext();

    try {
      const response = await fetch(this.backendUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_message: userQuery,
          dashboard_data: dashboardData
        })
      });

      const data = await response.json();
      return data.reply;
    } catch (error) {
      console.error('Erro na IA Admin:', error);
      return 'Erro ao conectar com o co-piloto Python.';
    }
  }
};
