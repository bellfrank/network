document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('#edit').forEach(function(edit){
        edit.onclick = function(){
            console.log(this.dataset)
            console.log("update")
            this.parentElement.style.display = 'none';
            form = this.parentElement.parentElement.querySelector('form')
            form.style.display = 'block';

            form.querySelector('button').onclick = function(){
                data = form.querySelector('#update-post');
                console.log("clicked save");
                console.log("update");
                console.log(data.value);
                form.style.display = 'none';

                return false;
            }
            this.parentElement.style.display = 'block';
            

            // prevents page from scrolling to the top when clicked
            return false;
            // element.parentElement.style.background = 'lightgreen';
            // document.querySelector('.post').style.background = 'lightgreen';
        }
    })
})



document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('#heart').forEach(function(heart){
        heart.onclick = function(){
            console.log(this.dataset)
            this.style.color = 'red';
            console.log("nice");
            console.log("update");
            
            // // somehow learn how to fetch the like count of this post and console log it
            // fetch('https://api.exchangeratesapi.io/latest?base=USD')
            // // Put response into json form
            // .then(response => response.json())
            // .then(data => {
    
            // })
            // // Catch any errors and log them to the console
            // .catch(error => {
            //     console.log('Error:', error);
            // });

            // this implementation of liking doesn't work :(

            document.querySelectorAll("#likes").forEach(function(likes){
                likes.onclick = function(){
                    console.log(this);
                    this.innerHTML = "2 likes";
                }
            })
            
            // prevents page from scrolling to the top when clicked
            return false;
        }
    })
})

function load_print() {
    console.log(document.querySelectorAll('#edit'));
}