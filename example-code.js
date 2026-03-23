// 改进后的函数
function calculateTotal(items) {
    if (!Array.isArray(items)) {
        throw new TypeError('items must be an array');
    }
    
    return items.reduce((total, item) => {
        if (!item || typeof item.price !== 'number' || typeof item.quantity !== 'number') {
            throw new Error('Invalid item: missing price or quantity');
        }
        if (item.price < 0 || item.quantity < 0) {
            throw new Error('Price and quantity must be non-negative');
        }
        return total + (item.price * item.quantity);
    }, 0);
}
