
    window.onload = function () {
        var length = {{ news.count }};
        for(i=1;i<=length;i++)
        $("#inner"+i).hide();
    };




    function senddata(id)
    {
       var id = Number(id);
       var length = {{ news.count }};
       for(i=1;i<=length;i++)
        $("#inner"+i).hide();

        $("#inner"+id).show();


        $.ajax({
         url: '/views/',
         type : 'post',
         dataType: 'json',
         data: {id: id,csrfmiddlewaretoken: '{{ csrf_token }}'},
         success: function(data) {
            console.log("viewd");
         },
         failure: function(data) {
            alert('error');
        }
    });//ajax




        return false;
    }

    function addupvotes(id)
    {
        console.log(id.id);
        var myid = id;
        $.ajax({
         url: '/upvote/',
         type : 'post',
         dataType: 'json',
         data: {id: id.id,csrfmiddlewaretoken: '{{ csrf_token }}'},
         success: function(data) {
            console.log(data.data);
              $(myid).prop('value', 'Upvotes '+data.data);
         },
         failure: function(data) {
            alert('error');
        }
    });//ajax



        return false;
    }

    function adddownvotes(id)
    {
        console.log(id);
        var myid = id;

        $.ajax({
         url: '/downvote/',
         type : 'post',
         dataType: 'json',
         data: {id: id.id,csrfmiddlewaretoken: '{{ csrf_token }}'},
         success: function(data) {
            console.log(data.data);
              $(myid).prop('value', 'Downvotes '+data.data);
         },
         failure: function(data) {
            alert('error');
        }
    });//ajax


        return false;
    }
