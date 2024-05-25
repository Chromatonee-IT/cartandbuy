
    new Autocomplete('#autocomplete', {
        search: input =>{
            var element = document.getElementById("search").closest("div")
            if (document.activeElement === document.querySelector('input')) { 
                element.style.zIndex = "10000000000000000";
            }
            else{
                element.style.zIndex = "0";
            }
            document.addEventListener('click', function(event) {
                if (event.target !== input) {
                    element.style.zIndex = "0";
                }
                else{
                    element.style.zIndex = "10000000000000000";
                }
            });
            const url = `/product_search/${(input)}/`
            return new Promise(resolve => {
                fetch(url)
                    .then(response=>response.json())
                    .then(data=>{
                        resolve(data.data)
                    })
            })
        },
        getResultValue: result => result.product,
        renderResult : (result, props)=>{
            let group = ''
            if (result.index ){
                group = `<li class="group">Group</li>`
            }
            return `
            ${group}
            <a style="color: black !important; font-size:1.3rem;" href="/product_single/${result.id}/">
            <li ${props}>
                <div class="wiki-title">
                    ${result.product}
                </div>
            </li>
            </a>
            `
        }
    })
    new Autocomplete('#autocomplete-mobile', {
        search: input =>{
            const url = `/product_search/${(input)}/`
            return new Promise(resolve => {
                fetch(url)
                    .then(response=>response.json())
                    .then(data=>{
                        resolve(data.data)
                    })
            })
        },
        getResultValue: result => result.product,
        renderResult : (result, props)=>{
            let group = ''
            if (result.index ){
                group = `<li class="group">Group</li>`
            }
            return `
            ${group}
            <a style="color: white !important; font-size:1rem;" href="/product_single/${result.id}/">
            <li ${props}>
                <div class="wiki-title">
                    ${result.product}
                </div>
            </li>
            </a>
            `
        }
    })
    
function product_search(){
    var search_input = document.querySelectorAll('#search')[0];
    console.log(search_input.value)
    if (search_input.value.length >= 1){
        var search_url = window.location.origin + '/search-products/' + search_input.value + '/'
        window.location.href =search_url
    }
}

function product_search_mobile(){
    var search_input = document.querySelectorAll('#search-mobile')[0];
    console.log(search_input.value)
    if (search_input.value.length >= 1){
        var search_url = window.location.origin + '/search-products/' + search_input.value + '/'
        window.location.href =search_url
    }
}


function product_sorting(){
    var url = new URL(window.location.href);
    var search_params = url.searchParams;
    search_params.set('ordering',document.getElementById("orderby").value);
    url.search = search_params.toString();
    var new_url = url.toString();
    window.location.href = new_url;
}



function product_filter_price(value){
    var url = new URL(window.location.href);
    var search_param = url.searchParams;
    search_param.set('price',value);
    url.search = search_param.toString();
    var new_url = url.toString();
    window.location.href = new_url;
}


function product_filter_price_custom(){
    var min_ele = document.getElementById("min_price").value;
    var max_ele = document.getElementById("max_price").value;
    var value = min_ele + "-" + max_ele;
    product_filter_price(value);
}

function clean_filter(){
    var url = new URL(window.location.href);
    var search_param = url.searchParams;
    search_param.delete('price');
    url.search = search_param.toString();
    var new_url = url.toString();
    window.location.href = new_url;
}

async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
        return null;
    }
}



var QtyInput = (function () {
	var $qtyInputs = $(".qty-input");

	if (!$qtyInputs.length) {
		return;
	}

	var $inputs = $qtyInputs.find(".product-qty");
	var $countBtn = $qtyInputs.find(".qty-count");
	var qtyMin = parseInt($inputs.attr("min"));
	var qtyMax = parseInt($inputs.attr("max"));

	$inputs.change(function () {
		var $this = $(this);
		var $minusBtn = $this.siblings(".qty-count--minus");
		var $addBtn = $this.siblings(".qty-count--add");
		var qty = parseInt($this.val());



		if (isNaN(qty) || qty <= qtyMin) {
			$this.val(qtyMin);
			$minusBtn.attr("disabled", true);
		} else {
			$minusBtn.attr("disabled", false);
			
			if(qty >= qtyMax){
				$this.val(qtyMax);
				$addBtn.attr('disabled', true);
			} else {
				$this.val(qty);
				$addBtn.attr('disabled', false);
			}
		}
	});

	$countBtn.click(function () {
		var operator = this.dataset.action;
		var $this = $(this);
		var $input = $this.siblings(".product-qty");
		var qty = parseInt($input.val());
        var item_id = $input.attr("id")
		if (operator == "add") {
			qty += 1;
            if (!isNaN(item_id)){
                var priceText = document.getElementsByName("product_price-"+item_id)[0].textContent;
                var price = parseFloat(priceText.replace('₹', ''));
                var subtotalelement = document.getElementsByName("product_subtotal-"+item_id)[0];
                var sub_total_Element = document.getElementById("sub_total");
                var total_Element = document.getElementById("total");
                var sub_total_Element_text = document.getElementById("sub_total").textContent;
                var subtotal_main = parseFloat(sub_total_Element_text.replace('₹', ''));
                var total_Element_text = document.getElementById("total").textContent;
                var total_main = parseFloat(total_Element_text.replace('₹', ''));
                var subtotalText = document.getElementsByName("product_subtotal-"+item_id)[0].textContent;
                var subtotal = parseFloat(subtotalText.replace('₹', ''));
                subtotalelement.textContent = '₹' + (subtotal + price);
                sub_total_Element.textContent = '₹' + (subtotal_main + price);
                total_Element.textContent = '₹' + (total_main + price);
                var baseUrl = window.location.origin;
                var url= baseUrl + '/increase_cart_count/' + item_id + '/';
                fetchData(url);
            }

			if (qty >= qtyMin + 1) {
				$this.siblings(".qty-count--minus").attr("disabled", false);
			}

			if (qty >= qtyMax) {
				$this.attr("disabled", true);
			}
		} else {
			qty = qty <= qtyMin ? qtyMin : (qty -= 1);
            if (!isNaN(item_id)){
                var priceText = document.getElementsByName("product_price-"+item_id)[0].textContent;
                var price = parseFloat(priceText.replace('₹', ''));
                var subtotalelement = document.getElementsByName("product_subtotal-"+item_id)[0];
                var sub_total_Element = document.getElementById("sub_total");
                var total_Element = document.getElementById("total");
                var sub_total_Element_text = document.getElementById("sub_total").textContent;
                var subtotal_main = parseFloat(sub_total_Element_text.replace('₹', ''));
                var total_Element_text = document.getElementById("total").textContent;
                var total_main = parseFloat(total_Element_text.replace('₹', ''));
                var subtotalText = document.getElementsByName("product_subtotal-"+item_id)[0].textContent;
                var subtotal = parseFloat(subtotalText.replace('₹', ''));
                subtotalelement.textContent = '₹' + (subtotal - price);
                sub_total_Element.textContent = '₹' + (subtotal_main - price);
                total_Element.textContent = '₹' + (total_main - price);
                var baseUrl = window.location.origin;
                var url= baseUrl + '/decrease_cart_count/' + item_id + '/';
                fetchData(url);
            }
			if (qty == qtyMin) {
				$this.attr("disabled", true);
			}

			if (qty < qtyMax) {
				$this.siblings(".qty-count--add").attr("disabled", false);
			}
		}

		$input.val(qty);
	});
})();




var QtyInput = (function () {
	var $qtyInputs = $("#product-qty-input");

	if (!$qtyInputs.length) {
		return;
	}

	var $inputs = $qtyInputs.find("#product-qty-count");
	var $countBtn = $qtyInputs.find("#qty-count");
	var qtyMin = parseInt($inputs.attr("min"));
	var qtyMax = parseInt($inputs.attr("max"));

	$inputs.change(function () {
		var $this = $(this);
		var $minusBtn = $this.siblings("#qty-count--minus-count");
		var $addBtn = $this.siblings("#qty-count--add-count");
		var qty = parseInt($this.val());

		if (isNaN(qty) || qty <= qtyMin) {
			$this.val(qtyMin);
			$minusBtn.attr("disabled", true);
		} else {
			$minusBtn.attr("disabled", false);
			
			if(qty >= qtyMax){
				$this.val(qtyMax);
				$addBtn.attr('disabled', true);
			} else {
				$this.val(qty);
				$addBtn.attr('disabled', false);
			}
		}
	});

	$countBtn.click(function () {
		var operator = this.dataset.action;
		var $this = $(this);
		var $input = $this.siblings(".product-qty");
		var qty = parseInt($input.val());

		if (operator == "add") {
			qty += 1;
			if (qty >= qtyMin + 1) {
				$this.siblings(".qty-count--minus").attr("disabled", false);
			}

			if (qty >= qtyMax) {
				$this.attr("disabled", true);
			}
		} else {
			qty = qty <= qtyMin ? qtyMin : (qty -= 1);
			
			if (qty == qtyMin) {
				$this.attr("disabled", true);
			}

			if (qty < qtyMax) {
				$this.siblings(".qty-count--add").attr("disabled", false);
			}
		}

		$input.val(qty);
	});
})();


function addToCart(){
    var all_colors = document.querySelectorAll(".color");
    var activecolor = document.querySelectorAll(".color.active");

    var all_sizes = document.querySelectorAll(".size");
    var active_size = document.querySelectorAll(".size.active");

    var product_id = document.getElementById("product_id").value;
    var count = document.getElementById("count").value;

    if (all_colors.length > 0){
        if (activecolor[0]){
            var cart_url = window.location.origin + '/add_to_cart/' + `${product_id}` + '/' + '?color=' + activecolor[0].id;
            if (all_sizes.length > 0){
                cart_url += '&size=' + active_size[0].id;
            }
        }else{
            window.alert("Please select color and size.");
        }
    }
    else if (all_sizes.length > 0){
        var cart_url = window.location.origin + '/add_to_cart/' + `${product_id}` + '/' + '?size=' + active_size[0].id;
    }
    else{
        var cart_url = window.location.origin + '/add_to_cart/' + `${product_id}` + '/';
    } 

    if (count >1){
        cart_url += '&quantity=' + count;
    }
    console.log(cart_url);
    window.location.href = cart_url;

  }
  document.getElementById("addtocart").addEventListener("click", addToCart);


  function show_hide_menu() {
    $(".menu-container").slideToggle("slow", function() {
      $(".cross-btn").toggle();
      $(".hamburger-btn").toggle();
    });
  };



  