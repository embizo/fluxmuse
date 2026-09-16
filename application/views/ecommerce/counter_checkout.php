<?php include(APPPATH.'views/ecommerce/store_style.php'); ?>
<div id="put_script"></div>
<section class="section">
	<div class="section-body mt-2">

		<div class="row">
			<div class="col-12 col-md-6">
				<div class="card" style="border:1px solid #dee2e6">
					<div class="card-header">
						<h6 class="full_width"><?php echo $this->lang->line("Find an existing order"); ?></h6>
					</div>
					<div class="card-body">
						<div class="input-group">
							<input type="text" class="form-control" id="search_query" placeholder="<?php echo $this->lang->line("Cart ID, phone number, or transaction reference"); ?>">
							<div class="input-group-append">
								<button class="btn btn-primary" type="button" id="search_button"><i class="fas fa-search"></i> <?php echo $this->lang->line("Search"); ?></button>
							</div>
						</div>
						<div id="search_results" class="mt-3"></div>
					</div>
				</div>
			</div>

			<div class="col-12 col-md-6">
				<div class="card" style="border:1px solid #dee2e6">
					<div class="card-header">
						<h6 class="full_width"><?php echo $this->lang->line("Or start a walk-in sale"); ?></h6>
					</div>
					<div class="card-body">
						<div class="form-group">
							<label><?php echo $this->lang->line("Customer phone (optional, needed for a pay link/QR)"); ?></label>
							<input type="text" class="form-control" id="buyer_mobile">
						</div>
						<button class="btn btn-success" type="button" id="start_sale_button"><i class="fas fa-cash-register"></i> <?php echo $this->lang->line("Start Walk-in Sale"); ?></button>
					</div>
				</div>
			</div>
		</div>

		<div class="row mt-3" id="active_sale_block" style="display:none">
			<div class="col-12 col-md-7">
				<div class="card" style="border:1px solid #dee2e6">
					<div class="card-header">
						<h6 class="full_width"><?php echo $this->lang->line("Products"); ?></h6>
					</div>
					<div class="card-body" style="max-height:520px;overflow-y:auto">
						<div class="row">
							<?php foreach($product_list as $product) : ?>
							<div class="col-6 col-md-4 mb-3">
								<div class="card counter_product" data-id="<?php echo $product['id']; ?>" data-price="<?php echo $product['sell_price']; ?>" style="cursor:pointer;border:1px solid #dee2e6">
									<div class="card-body text-center p-2">
										<div style="font-size:13px" class="text-truncate"><?php echo htmlspecialchars($product['product_name']); ?></div>
										<div class="text-primary"><?php echo mec_number_format($product['sell_price'],isset($ecommerce_config['decimal_point']) ? $ecommerce_config['decimal_point'] : 2,isset($ecommerce_config['thousand_comma']) ? $ecommerce_config['thousand_comma'] : '0'); ?></div>
									</div>
								</div>
							</div>
							<?php endforeach; ?>
						</div>
					</div>
				</div>
			</div>

			<div class="col-12 col-md-5">
				<div class="card" style="border:1px solid #dee2e6">
					<div class="card-header">
						<h6 class="full_width"><?php echo $this->lang->line("Current Sale"); ?> #<span id="active_cart_id"></span></h6>
					</div>
					<div class="card-body">
						<div id="cart_items_block"><?php echo $this->lang->line("Tap a product to add it."); ?></div>
						<hr>
						<button class="btn btn-block btn-primary" type="button" id="generate_pay_link_button"><i class="fas fa-qrcode"></i> <?php echo $this->lang->line("Generate Pay Link / QR"); ?></button>
						<div id="pay_link_block" class="text-center mt-3"></div>
						<hr>
						<p class="text-muted small"><?php echo $this->lang->line("No card machine? Have the customer scan the QR above and pay on their own phone, or use Cash/Manual below."); ?></p>
						<button class="btn btn-block btn-outline-secondary" type="button" onclick="parent.location.reload();"><?php echo $this->lang->line("Done"); ?></button>
					</div>
				</div>
			</div>
		</div>

	</div>
</section>

<script>
var base_url="<?php echo site_url(); ?>";
var store_id = <?php echo (int)$store_id; ?>;
var active_cart_id = 0;
var active_subscriber_id = "";

$(document).ready(function($){

	$('#search_button').on('click', function(){
		var query = $('#search_query').val();
		if(query=="") return;
		$.ajax({
			type:'POST',
			url: base_url+"ecommerce/counter_search_order",
			data:{store_id:store_id, query:query},
			dataType:'JSON',
			success:function(response){
				var html = "";
				if(response.status=='1'){
					response.orders.forEach(function(order){
						html += "<div class='card mb-2'><div class='card-body p-2'>";
						html += "<b>#"+order.id+"</b> - "+order.status+" - "+order.payment_amount+" "+order.currency;
						html += " <button class='btn btn-sm btn-primary float-right resume_order' data-cart_id='"+order.id+"' data-subscriber_id='"+order.subscriber_id+"'><?php echo $this->lang->line("Resume"); ?></button>";
						html += "</div></div>";
					});
				} else {
					html = "<div class='alert alert-warning'>"+response.message+"</div>";
				}
				$('#search_results').html(html);
			}
		});
	});

	$(document).on('click', '.resume_order', function(){
		active_cart_id = $(this).data('cart_id');
		active_subscriber_id = $(this).data('subscriber_id');
		$('#active_cart_id').text(active_cart_id);
		$('#active_sale_block').show();
	});

	$('#start_sale_button').on('click', function(){
		$.ajax({
			type:'POST',
			url: base_url+"ecommerce/counter_start_sale",
			data:{store_id:store_id, buyer_mobile:$('#buyer_mobile').val()},
			dataType:'JSON',
			success:function(response){
				if(response.status=='1'){
					active_subscriber_id = response.subscriber_id;
					active_cart_id = 0;
					$('#active_cart_id').text("("+"<?php echo $this->lang->line("new"); ?>"+")");
					$('#active_sale_block').show();
					$('#cart_items_block').html("<?php echo $this->lang->line("Tap a product to add it."); ?>");
				} else {
					swal('<?php echo $this->lang->line("Error"); ?>', response.message, 'error');
				}
			}
		});
	});

	$(document).on('click', '.counter_product', function(){
		var product_id = $(this).data('id');
		var mydata = {
			product_id: product_id,
			action: 'add',
			subscriber_id: active_subscriber_id
		};
		$.ajax({
			type:'POST',
			url: base_url+"ecommerce/update_cart_item",
			data:{mydata: JSON.stringify(mydata)},
			dataType:'JSON',
			success:function(response){
				if(response.status=='0'){
					swal('<?php echo $this->lang->line("Error"); ?>', response.message, 'error');
					return;
				}
				if(response.cart_data && response.cart_data.cart_id) active_cart_id = response.cart_data.cart_id;
				$('#active_cart_id').text(active_cart_id);
				refresh_cart();
			}
		});
	});

	function refresh_cart()
	{
		if(!active_cart_id) return;
		$.ajax({
			type:'POST',
			url: base_url+"ecommerce/counter_search_order",
			data:{store_id:store_id, query:active_cart_id},
			dataType:'JSON',
			success:function(response){
				if(response.status!='1') return;
				var order = response.orders[0];
				if(!order) return;
				var html = "<table class='table table-sm'>";
				order.items.forEach(function(item){
					html += "<tr><td>"+item.product_name+"</td><td>x"+item.quantity+"</td><td>"+item.unit_price+"</td></tr>";
				});
				html += "</table><b><?php echo $this->lang->line("Total"); ?>: "+order.payment_amount+" "+order.currency+"</b>";
				$('#cart_items_block').html(html);
			}
		});
	}

	$('#generate_pay_link_button').on('click', function(){
		if(!active_cart_id){
			swal('<?php echo $this->lang->line("Error"); ?>', "<?php echo $this->lang->line("Add at least one product first."); ?>", 'error');
			return;
		}
		$.ajax({
			type:'POST',
			url: base_url+"ecommerce/counter_generate_pay_link",
			data:{cart_id:active_cart_id, subscriber_id:active_subscriber_id, buyer_mobile:$('#buyer_mobile').val()},
			dataType:'JSON',
			success:function(response){
				if(response.status!='1'){
					swal('<?php echo $this->lang->line("Error"); ?>', response.message, 'error');
					return;
				}
				var html = "";
				if(response.qr_url) html += "<img style='width:200px' src='"+response.qr_url+"'><br>";
				if(response.pay_link) html += "<a href='"+response.pay_link+"' target='_blank'><?php echo $this->lang->line("Open Pay Link"); ?></a><br>";
				if(response.whatsapp_sent) html += "<div class='alert alert-success mt-2'><i class='fab fa-whatsapp'></i> <?php echo $this->lang->line("Sent to the customer's WhatsApp automatically."); ?></div>";
				else if(response.whatsapp_link) html += "<a class='btn btn-sm btn-success mt-2' href='"+response.whatsapp_link+"' target='_blank'><i class='fab fa-whatsapp'></i> <?php echo $this->lang->line("Send via WhatsApp"); ?></a>";
				if(response.message) html += "<div class='alert alert-info mt-2'>"+response.message+"</div>";
				$('#pay_link_block').html(html);
			}
		});
	});

});
</script>
