//-------------Add comment--------
var commentBtns = document.getElementsByClassName('add-comment')

for (i = 0; i < commentBtns.length; i++) {
    commentBtns[i] .addEventListener('click', function(){
        var documentId = this.dataset.document
        var action = this.dataset.action
        var memo = document.getElementById("memo").value;

        console.log('DocumentId:',documentId, 'Action:', action, 'Memo:', memo)

        console.log('USER:', user)
        if(user == 'AnonymousUser'){
            console.log('User is not authenticate')
            }else{
                addComment(documentId, action, memo)
            } 
    })
}

function addComment(documentId, action, memo){
    console.log('User logged in OK')
    var url = '/getcomment/'
    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,         
        },
        body:JSON.stringify({'documentId': documentId, 'action':action, 'memo': memo})
    })
    .then((response) => {
        return response.json();
    })
    .then((data => {
        console.log('Data:', data)
        location.reload()
    }));
}