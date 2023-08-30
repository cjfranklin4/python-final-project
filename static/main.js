document.addEventListener('DOMContentLoaded', function () {
    const toggleCartButton = document.getElementById('toggleCartButton');
    const cartContainer = document.querySelector('#shopping-cart');

    toggleCartButton.addEventListener('click', function () {
        console.log("I work")
        cartContainer.classList.toggle('active');
    });
});

function full_cart() {
    var cartSize = document.querySelectorAll('.cart-item.shop-page').length;
    //console.log("I WORK", cartSize)
    if (cartSize >= 3) {
        alert('Cart is full! Please remove items before adding more.');
    }
}