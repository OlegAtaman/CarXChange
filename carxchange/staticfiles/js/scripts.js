// IN PROGRESS

// var csrftoken = getCookie('csrftoken');
//             async function respfunc(data, csrftoken) {
//                     const result = await fetch('{{ request.path }}/changeuser', {method: 'POST',headers:{"Content-Type":"application/json", "X-CSRFToken":csrftoken}, body:JSON.stringify(data)}); 
//                     return result.json();
//             };
//             function getCookie(name) {
//                 var cookieValue = null;
//                 if (document.cookie && document.cookie !== '') {
//                     var cookies = document.cookie.split(';');
//                     for (var i = 0; i < cookies.length; i++) {
//                     var cookie = cookies[i].trim();
//                     if (cookie.substring(0, name.length + 1) === name + '=') {
//                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                         break;
//                     }
//                     }
//                 }
//                 return cookieValue;
//             };

//             function switchtofield (field) {
//                 var parent = field.parentElement;
//                 if (parent.id == 'name') {
//                     getbackval = parent.textContent.trim();
//                 } else if (parent.id == 'contacts') {
//                     getbackval_raw = parent.textContent.trim();
//                     start = getbackval_raw.indexOf('Контакти: ');
//                     getbackval = getbackval_raw.substring(10, getbackval_raw.length).trim();
//                 } else if (parent.id == 'region') {
//                     getbackval_raw = parent.textContent.trim();
//                     getbackval = getbackval_raw.substring(9, getbackval_raw.length).trim();
//                 };
//                 parent.innerHTML = "";
//                 reg_html = `
//                 <select id='get_new_region' autocomplete="country">
//                     {% for option in reg_choices %}
//                         <option value="{{ option.0 }}">{{ option.1 }}</option>
//                     {% endfor %}
//                 </select>
//                 `
//                 if (parent.id == 'name') {
//                     parent.innerHTML = "<input id='get_new_name' type='text' class='profileeditinput'><button style='width:170px;margin:5px' id='name-edit-b' onclick='editfield(this)' class='profileeditbutton'>Підтвердити</button><button style='background:grey' class='profileeditbutton' onclick='setback(this, getbackval)'>Скасувати</button>"
//                 } else if (parent.id == 'contacts') {
//                     parent.innerHTML = "<input id='get_new_contacts' type='text' class='profileeditinput'><button style='width:170px;margin:5px' id='contacts-edit-b' onclick='editfield(this)' class='profileeditbutton'>Підтвердити</button><button style='background:grey' class='profileeditbutton' onclick='setback(this, getbackval)'>Скасувати</button>"
//                 } else if (parent.id == 'region') {
//                     parent.innerHTML = reg_html+"<button style='width:170px;margin:5px' id='region-edit-b' onclick='editfield(this)' class='profileeditbutton'>Підтвердити</button><button style='background:grey' class='profileeditbutton' onclick='setback(this, getbackval)'>Скасувати</button>"
//                 };
//             };
//             function setback(field, val) {
//                 var parent = field.parentElement;
//                 parent.innerHTML = "";
//                 if (parent.id == 'name') {
//                     parent.innerHTML = val + "<a class='editprofilejs' onclick='switchtofield(this)'><img class='editprofilejsimg' style='height: 30px;' src='{% static 'images/edit.png' %}'></a>"
//                 } else if (parent.id == 'contacts') {
//                     parent.innerHTML = "Контакти: " + val + "<a class='editprofilejs' onclick='switchtofield(this)'><img class='editprofilejsimg' src='{% static 'images/edit.png' %}'></a>"
//                 } else if (parent.id == 'region') {
//                     parent.innerHTML = "Локація: " + val + "<a class='editprofilejs' onclick='switchtofield(this)'><img class='editprofilejsimg' src='{% static 'images/edit.png' %}'></a>"
//                 };
//             };
//             function editfield(button) {
//                 if (button.id == 'name-edit-b') {
//                     var arg = document.getElementById('get_new_name').value;
//                     respfunc({"full_name": arg})
//                     button.parentElement.innerHTML = arg + "<a class='editprofilejs' onclick='switchtofield(this)'><img class='editprofilejsimg' style='height: 30px;' src='{% static 'images/edit.png' %}'></a>"
//                 } else if (button.id == 'contacts-edit-b') {
//                     var arg = document.getElementById('get_new_contacts').value;
//                     respfunc({"contacts": arg})
//                     button.parentElement.innerHTML = "Контакти: " + arg + "<a class='editprofilejs' onclick='switchtofield(this)'><img class='editprofilejsimg' src='{% static 'images/edit.png' %}'></a>"
//                 } else if (button.id == 'region-edit-b') {
//                     var arg = document.getElementById('get_new_region').value;
//                     var result = respfunc({"region": arg});
//                     console.log(result)
//                     var val = result.then(function(result) {
//                         var updtValue = result.updt;
//                         button.parentElement.innerHTML = "Локація: " + updtValue + "<a class='editprofilejs' onclick='switchtofield(this)'><img class='editprofilejsimg' src='{% static 'images/edit.png' %}'></a>" 
//                     });
//                 };
                
//             }