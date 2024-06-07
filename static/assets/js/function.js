// Adding review

console.log('working....')



$("#commentForm").submit(function(e){
    e.preventDefault();


    $.ajax({
        // data is what the user is passing in the form.
        data: $(this).serialize(),

        // getting the method attribute that has post as it value
        method: $(this).attr("method"),

        url: $(this).attr("action"),
        dataType : "json",

        success: function(res){
            console.log("Review saved to DB.....")
            if(res.bool == true){
                $("#review-res").html("Review added successfully.")
                // $(".hide-comment-form").hide()
                $(".hide-review").hide()
        
                let rating = res.context.rating; // Assuming res.context.rating is the number of stars to display
                let starsHtml = '';
                for (let i =   1; i <= rating; i++) {
                    starsHtml += `<li><a href="#"><i class="ion-android-star"></i></a></li>`;
                }
        
                // Try to parse the date, and if it's invalid, use the current date as a fallback
                let date = new Date(res.context.date);
                if (isNaN(date.getTime())) {
                    date = new Date(); // Use the current date as a fallback
                }
        
                let formattedDate = date.toLocaleString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric' });
        
                let _html = `<div class="reviews_comment_box">
                    <div class="comment_thmb">
                        <img src="${res.context.staticUrl}/assets/img/blog/comment2.jpg" alt="">
                    </div>
                    <div class="comment_text">
                        <div class="reviews_meta">
                            <div class="star_rating">
                                <ul>${starsHtml}</ul>
                            </div>
                            <p><strong>${res.context.user}</strong> - ${formattedDate}</p>
                            <span>${res.context.review}</span>
                        </div>
                    </div>
                </div>`;
        
                $(".reviews_wrapper").prepend(_html);
            }
        }
    })
})




// $(document).ready(function(){
//     $(".filter-link").on("click", function(){
//         let filter_object = {}

        // Get the data-filter value of the clicked element
        // let filter_key = $(this).data("filter");

        // Use the filter_key to select li elements with matching data-filter attribute
//         filter_object[filter_key] = Array.from($(`li[data-filter='${filter_key}']`)).map(function(element){
//             return element.id;
//         });

//         console.log(filter_object);
//     });
// });




$(document).ready(function(){

   $(".add-to-cart-btn").on("click", function(){
    let this_val = $(this)
    let index = this_val.attr("data-index");
    let quantity = $(".product-quantity-"+ index).val();
    let product_title = $(".product-title-"+ index).val();
    let product_image = $(".product-image-"+ index).val();
    let product_pid = $(".product-pid-"+ index).val();
    let product_id = $(".product-id-"+ index).val();
    let product_price = $(".current-product-price-"+ index).text();
    // let product_price = this_val.attr("data-price");
    

    // console.log("Quantity ", quantity);
    // console.log("Title ", product_title);
    console.log("ID ", product_id);
    console.log("Price ", product_price);
    // console.log("Image ", product_image);
    // console.log("PID ", product_pid);
    // console.log("Index ", index);
    // console.log('this : ', this_val);

    $.ajax({
        url: '/add-to-cart',
        data:{
             'id':product_id,
             'pid':product_pid,
             'image':product_image,
             'qty':quantity,
             'title':product_title,
             'price':product_price
        },
        dataType: 'json',
        beforeSend: function(){
            console.log('Adding Product to cart');

        },
        success: function(response){
            this_val.html("✔")
            console.log('Added Product to cart....');
            $(".cart-items-count").text(response.totalcartitems);
        }

    })
})


// Deleting product from cart without reloading the page.
        $(".delete-product").on("click", function(){
            let product_id = $(this).attr("data-product");
            let this_val = $(this);
            console.log("Product ID: ",product_id);

            $.ajax({
                url: "/delete-from-cart",
                data:{
                    "id": product_id
                },

                dataType: "json",
                beforeSend: function(){
                    this_val.hide();
                },

                success: function(response){
                    this_val.show()
                    $(".cart-items-count").text(response.totalcartitems);
                    $("#cart-list").html(response.data)
                }
            })
        }) 

        

        $(".update-product").on("click", function(){
            let product_id = $(this).attr("data-product");
            let product_quantity = $('.product-qty-'+product_id).val();
            console.log("Product ID: ", product_id);
            console.log("Product QTY: ", product_quantity);
          
            $.ajax({
              url: "/update-cart", // Replace with your actual URL
              data:{
                id: product_id,
                qty: product_quantity
              },
              dataType: "json",
              beforeSend: function(){
                $(this).hide(); // Hide the update element (optional)
              },
              success: function(response){
                $(this).show(); // Show the update element again (optional)
                $(".cart-items-count").text(response.totalcartitems);
                $("#cart-list").html(response.data);
              },
              error: function(jqXHR, textStatus, errorThrown) {
                console.error("AJAX Error:", textStatus, errorThrown); // Log errors
              }
            });
          });
          
});


// * Add to cart









// $("#add-to-cart-btn").on("click", function(){
//     let quantity = $("#product-quantity").val()
//     let product_title = $(".product-title").val()
//     let product_id = $(".product-id").val()
//     let product_price = $("#current-product-price").text()
//     let this_val = $(this)

//     // console.log(quantity);
//     // console.log(product_title);
//     // console.log(product_id);
//     // console.log(product_price);
//     console.log('this : ', this_val);

//     $.ajax({
//         url: '/add-to-cart',
//         data:{
//              'id':product_id,
//              'qty':quantity,
//              'title':product_title,
//              'price':product_price
//         },
//         dataType: 'json',
//         beforeSend: function(){
//             console.log('Adding Product to cart');

//         },
//         success: function(response){
//             this_val.html("Item added to cart")
//             console.log('Added Product to cart....');
//             $(".cart-items-count").text(response.totalcartitems);
//         }

//     })
// })