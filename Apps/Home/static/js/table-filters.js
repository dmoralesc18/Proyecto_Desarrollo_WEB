// Simple table text filter utility
// Usage: add an input with [data-table-filter="#tableId"] and it will filter rows on input
(function(){
  function normalize(s){
    return (s || '').toString().toLowerCase();
  }
  function attach(el){
    var targetSel = el.getAttribute('data-table-filter');
    if (!targetSel) return;
    var table = document.querySelector(targetSel);
    if (!table) return;
    var tbody = table.tBodies && table.tBodies[0];
    if (!tbody) return;
    el.addEventListener('input', function(){
      var q = normalize(el.value);
      var rows = Array.prototype.slice.call(tbody.rows || []);
      rows.forEach(function(tr){
        var txt = normalize(tr.innerText || tr.textContent);
        tr.style.display = q && txt.indexOf(q) === -1 ? 'none' : '';
      });
    });
  }
  function init(){
    document.querySelectorAll('[data-table-filter]').forEach(attach);
  }
  if (document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

