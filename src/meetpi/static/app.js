(function(){
  function copyToClipboard(text){
    if(navigator.clipboard && navigator.clipboard.writeText){
      return navigator.clipboard.writeText(text);
    }
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.left = '-9999px';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); } catch(e){}
    document.body.removeChild(ta);
    return Promise.resolve();
  }

  document.addEventListener('DOMContentLoaded', function(){
    var btn = document.getElementById('copyBtn');
    var msg = document.getElementById('copyMsg');
    if(!btn) return;
    btn.addEventListener('click', function(){
      var url = btn.getAttribute('data-url');
      copyToClipboard(url).then(function(){
        if(msg){
          msg.textContent = 'Link copied to clipboard';
          msg.style.opacity = '1';
          setTimeout(function(){ msg.style.opacity = '0'; }, 2000);
        }
      });
    });
  });
})();
