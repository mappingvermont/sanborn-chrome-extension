(function() {

window.onload = function() {
  
  var rand = sheets[Math.floor(Math.random() * sheets.length)];
  var label = toTitleCase(rand.city.replace('_', ' ')) + ', ' + rand.year;

  document.body.style.backgroundImage = 'url(' + rand.loc_url + ')';
  document.getElementById('label').innerHTML = label
  
}

function toTitleCase(str)
{
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}
  
})();
