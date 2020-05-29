var acceptBtns = document.getElementsByClassName('accept-doc')

for (i = 0; i < acceptBtns.length; i++) {
    acceptBtns[i] .addEventListener('click', function(){
        var documentId = this.dataset.document
        var action = this.dataset.action
        console.log('DocumentId:',documentId, 'Action:', action)

        console.log('USER:', user)
        if(user == 'AnonymousUser'){
            console.log('User is not authenticate')
            }else{
                acceptedDocument(documentId, action)
            } 
    })
}

function acceptedDocument(documentId, action){
    console.log('User logged in OK')
    var url = '/accepted/'
    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,         
        },
        body:JSON.stringify({'documentId': documentId, 'action':action})
    })
    .then((response) => {
        return response.json();
    })
    .then((data => {
        console.log('Data:', data)
        location.reload()
    }));
}