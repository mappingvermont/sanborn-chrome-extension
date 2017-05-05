(function() {

window.onload = function() {
  
  var opt1 = {'label': 'Vergennes, 1892', 'url': 'http://tile.loc.gov/image-services/iiif/service:gmd:gmd375m:g3754m:g3754vm:g089531897:08953_1897-0002/full/pct:25/0/default.jpg'};
  var opt2 = {'label': 'Barton, 1811', 'url': 'http://tile.loc.gov/image-services/iiif/service:gmd:gmd375m:g3754m:g3754bm:g089031897:08903_1897-0001/full/pct:25/0/default.jpg'};
  var opt3 = {'label': 'Fair Haven, 1899', 'url': 'http://tile.loc.gov/image-services/iiif/service:gmd:gmd375m:g3754m:g3754fm:g089171897:08917_1897-0004/full/pct:25/0/default.jpg'};
  
  var myArray = [opt1, opt2, opt3]
  var rand = myArray[Math.floor(Math.random() * myArray.length)];
  
  document.body.style.backgroundImage = 'url(' + rand.url + ')';
  document.getElementById('label').innerHTML = rand.label;
  
}
  
})();
