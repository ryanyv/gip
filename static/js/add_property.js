// JS for add property photo gallery with reordering and preview

(function(){
  const input = document.getElementById('id_photos');
  const addBtn = document.getElementById('photosAddBtn');
  const gallery = document.getElementById('photosGallery');
  const overlay = document.getElementById('photosOverlay');
  const overlayGrid = document.getElementById('photosOverlayGrid');
  const overlayClose = document.getElementById('photosOverlayClose');
  if(!input || !addBtn || !gallery) return; // not on this page

  let files = [];

  function updateInput(){
    const dt = new DataTransfer();
    files.forEach(f => dt.items.add(f));
    input.files = dt.files;
  }

  function createThumb(file, idx){
    const div = document.createElement('div');
    div.className = 'relative w-24 h-24 rounded overflow-hidden cursor-move';
    const img = document.createElement('img');
    img.className = 'object-cover w-full h-full';
    img.src = URL.createObjectURL(file);
    div.appendChild(img);
    div.dataset.index = idx;
    return div;
  }

  function render(){
    gallery.innerHTML = '';
    files.forEach((f, i)=>{
      const t = createThumb(f, i);
      gallery.appendChild(t);
    });
    overlayGrid.innerHTML = '';
    files.forEach(f=>{
      const img = document.createElement('img');
      img.src = URL.createObjectURL(f);
      img.className = 'w-full h-64 object-cover rounded';
      overlayGrid.appendChild(img);
    });
  }

  addBtn.addEventListener('click', ()=> input.click());

  input.addEventListener('change', e=>{
    files = files.concat(Array.from(e.target.files));
    updateInput();
    render();
  });

  new Sortable(gallery, {
    animation: 150,
    onEnd: evt => {
      const [moved] = files.splice(evt.oldIndex, 1);
      files.splice(evt.newIndex, 0, moved);
      updateInput();
      render();
    }
  });

  gallery.addEventListener('click', ()=>{
    overlay.classList.remove('hidden');
  });
  overlayClose?.addEventListener('click', ()=> overlay.classList.add('hidden'));
  overlay.addEventListener('click', e=>{
    if(e.target === overlay) overlay.classList.add('hidden');
  });
})();
