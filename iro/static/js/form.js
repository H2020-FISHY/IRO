$("button").click(function(e) {
                e.preventDefault(); //to avoid reload
		const valueOfButton = $(this).attr("value");
                $.ajax({
                            type: "POST",
                            url: "/intents.html",
                            data: { 
                                "How can I get the value of the button tag??"
                                },
                            success: function(result) {
                                alert('ok');
                            },
                            error: function(result) {
                                alert('error');
                            }
                        });
                    });  

