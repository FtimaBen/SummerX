
(async function () {
    const output = document.createElement('div');
    const END$POINT = 'http://fatben.pythonanywhere.com/';
    const reviewNodes = document.querySelectorAll('.review-text-content span');
    const reviews = Array();
    const message = "<div class='remove_after'><h3 class='remove'>X</h3> <br> SummerX is loading the review, please wait</div>";
    const product = location.href.split('/')[3];
    let activePopup = true;

    output.className = 'output'
    output.innerHTML = message

    document.body.prepend(output)
    reviewNodes.forEach(reviewSpan => reviews.push(reviewSpan.innerText));

    if (reviewNodes.length == 0 || activePopup == false) return output.innerHTML = 'No reviews available for this product';

    await fetch(END$POINT, {
          method: 'POST',
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({'reviews': reviews}),
        })
        .then(response => response.json())
        .then(data => { 
          if (activePopup) output.outerHTML = data.template;

          document.querySelector('.remove').onclick = () => document.querySelector('.remove_after').outerHTML = "";
        })

        .catch(error => { output.innerHTML = "<div class='remove_after'><h3 class='remove'>X</h3> <br> SummerX is down right now </div>"  });

})()
