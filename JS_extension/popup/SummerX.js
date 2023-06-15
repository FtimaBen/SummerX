(function () {
    const summary = document.querySelector('summary');
    const review_card = document.querySelector('card');

    for (product in saved_reviews) {
        let new_card = review_card.cloneNode(True);
        console.log(prouct)

        new_card.querySelector('.btn').innerText = product
        new_card.querySelector('.card-body').innerText = saved_reviews[product];

        console.log(new_card)
        document.body.append(new_card);
    }
})()

