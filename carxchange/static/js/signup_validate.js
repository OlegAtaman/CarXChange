const form = document.getElementById('id_form')
const error_element = document.getElementById('error_element')

const username = document.getElementById('id_username')
const password1 = document.getElementById('id_password1')
const password2 = document.getElementById('id_password2')
const full_name = document.getElementById('id_full_name')
const contacts = document.getElementById('id_contacts')
const region = document.getElementById('id_region')
const picture = document.getElementById('id_picture')

const upperCaseString = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
const lowerCaseString = 'abcdefghijklmnopqrstuvwxyz';
const digitsString = '0123456789'

const checksimpliness = function(password) {
    let contains_lower = false
    let contains_upper = false
    let contains_digit = false
    for (let i=0; i < upperCaseString.length; i++) {
        if (password.includes(upperCaseString[i])) {
            contains_upper = true
            break
        }
    }
    for (let i=0; i < lowerCaseString.length; i++) {
        if (password.includes(lowerCaseString[i])) {
            contains_lower = true
            break
        }
    }
    for (let i=0; i < digitsString.length; i++) {
        if (password.includes(digitsString[i])) {
            contains_digit = true
            break
        }
    }
    if (contains_lower && contains_upper && contains_digit) {
        return true
    }
    return false
}

form.addEventListener('submit', (e) => {
    let messages = []
    if (password1.value.length < 8) {
        messages.push('Пароль занадто короткий!')
    }
    if (password1.value.length > 30) {
        messages.push('Пароль занадто довгий!')
    }
    if (password1.value != password2.value) {
        messages.push('Паролі не збігаються!')
    }
    if (username.value.toLowerCase().includes(password1.value.toLowerCase()) || password1.value.toLowerCase().includes(username.value.toLowerCase())) {
        messages.push('Пароль занадто схожий на логін!')
    }
    if (checksimpliness(password1.value) == false) {
        messages.push('Пароль має містити хоча б одну велику, малу літери та цифру!')
    }
    if (picture.files.length == 0) {
        messages.push('Фото не обране!')
    }
    if (messages.length > 0) {
        e.preventDefault()
        errorhtml = '<ul style="color:red">'
        for (let i=0; i < messages.length; i++) {
            errorhtml += '<li>'+ messages[i] +'</li>'
        }
        errorhtml += '</ul>'
        error_element.innerHTML = errorhtml
    };
})