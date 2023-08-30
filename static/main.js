function full_cart() {
    var cartSize = document.querySelectorAll('.cart-item.shop-page').length;
    console.log("I WORK", cartSize)
    if (cartSize >= 3) {
        alert('Cart is full! Please remove items before adding more.');
    }
}