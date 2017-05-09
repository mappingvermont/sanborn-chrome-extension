(function() {

window.onload = function() {
  
  var rand = sheets[Math.floor(Math.random() * sheets.length)];
  var label = toTitleCase(rand.city.replace('_', ' ')) + ' ' + rand.year + ', Sheet ' + rand.sheet_num;

  var content = '<a target="_blank" href="' + rand.gallery_url + '">' + label + '</a>'

  document.body.style.backgroundImage = 'url(' + rand.s3_url + ')';
  document.getElementById('label').innerHTML = content
  
}

function toTitleCase(str)
{
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}
  
})();
