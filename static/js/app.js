// Mobile Navbar Toggle (if not handled inline)
document.addEventListener('DOMContentLoaded', function () {
  const btn = document.getElementById('mobile-menu-button');
  const menu = document.getElementById('mobile-menu');
  const openIcon = document.getElementById('mobile-menu-icon-open');
  const closeIcon = document.getElementById('mobile-menu-icon-close');
  if (btn && menu && openIcon && closeIcon) {
    btn.addEventListener('click', function () {
      menu.classList.toggle('hidden');
      openIcon.classList.toggle('hidden');
      closeIcon.classList.toggle('hidden');
    });
  }

  // Gold ripple effect for all .button-gold elements
  document.querySelectorAll('.button-gold').forEach(btn => {
    btn.addEventListener('click', function (e) {
      btn.classList.add('ring-4', 'ring-[#E4B165]', 'transition');
      setTimeout(() => {
        btn.classList.remove('ring-4', 'ring-[#E4B165]');
      }, 300);
    });
  });

  // Brand color hover for anchor tags
  document.querySelectorAll('a').forEach(a => {
    a.addEventListener('mousedown', () => a.classList.add('text-gold'));
    a.addEventListener('mouseup', () => a.classList.remove('text-gold'));
    a.addEventListener('mouseleave', () => a.classList.remove('text-gold'));
  });

  // (Optional) Future: Dark mode toggle based on OS preference
  // if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
  //   document.body.classList.add('dark');
  // }

    /* ------------------------------------------------
       Quick‑view modal for property cards
    ------------------------------------------------ */
    const modal      = document.getElementById('propertyModal');
    const modalClose = document.getElementById('modalClose');
    const modalImg   = document.getElementById('modalImg');
    const modalTitle = document.getElementById('modalTitle');
    const modalLoc   = document.getElementById('modalLocation');
    const modalPrice = document.getElementById('modalPrice');
    const modalLink  = document.getElementById('modalLink');

    if (modal) {
      // open
      document.querySelectorAll('.property-card').forEach(card => {
        card.addEventListener('click', e => {
          if (e.target.closest('a, button')) return; // keep normal links/buttons working
          modalImg.src         = card.dataset.img || '';
          modalTitle.textContent = card.dataset.name || '';
          modalLoc.textContent   = card.dataset.location || '';
          modalPrice.textContent = card.dataset.price || '';
          modalLink.href         = card.dataset.url || '#';
          modal.classList.remove('hidden');
        });
      });
      // close
      const closeModal = () => modal.classList.add('hidden');
      modalClose?.addEventListener('click', closeModal);
      modal.addEventListener('click', e => {
        if (e.target === modal) closeModal();
      });
      window.addEventListener('keydown', e => {
        if (e.key === 'Escape') closeModal();
      });
    }
  /* -------------- Who dropdown -------------- */
  const whoInput     = document.getElementById('whoInput');
  const whoDropdown  = document.getElementById('whoDropdown');
  const whoHidden    = document.getElementById('guestsHidden');
  const whoCounts    = { adults:0, children:0, infants:0, pets:0 };

  window.toggleWhoDropdown = function(){
    if(whoDropdown) whoDropdown.classList.toggle('hidden');
  }

  window.updateWho = function(type, delta){
    if(!(type in whoCounts)) return;
    whoCounts[type] = Math.max(0, whoCounts[type] + delta);
    document.getElementById(`who-${type}`).textContent = whoCounts[type];
    // live summary
    const parts=[];
    if(whoCounts.adults)   parts.push(`${whoCounts.adults} adults`);
    if(whoCounts.children) parts.push(`${whoCounts.children} children`);
    if(whoCounts.infants)  parts.push(`${whoCounts.infants} infants`);
    if(whoCounts.pets)     parts.push(`${whoCounts.pets} pets`);
    whoInput.value = parts.length ? parts.join(', ') : 'Add guests';
    if(whoHidden){
      const total = whoCounts.adults + whoCounts.children + whoCounts.infants + whoCounts.pets;
      whoHidden.value = total > 0 ? total : '';
    }
  }

  // close on click outside
  window.addEventListener('click', e=>{
    if(!whoDropdown || !whoInput) return;
    if(!whoDropdown.contains(e.target) && !whoInput.contains(e.target)){
      whoDropdown.classList.add('hidden');
    }
  });
});

// Future: Image carousel, drag-drop, modals, map integration JS goes here.

/* -------------- Calendar dropdown (check‑in/out) -------------- */
const checkInInput   = document.querySelector('input[name="checkin"]');
const checkOutInput  = document.querySelector('input[name="checkout"]');
const calDropdown    = document.getElementById('calendarDropdown');
const calGrid        = document.getElementById('calendarGrid');
const calLabel       = document.getElementById('calMonthLabel');
const calPrev        = document.getElementById('calPrev');
const calNext        = document.getElementById('calNext');
const calApply       = document.getElementById('calApply');
const calClear       = document.getElementById('calClear');

let currentMonth = new Date(new Date().getFullYear(), new Date().getMonth(), 1); // first of this month
let startDate = null;
let endDate   = null;

/* -------- helpers for calendar ---------- */
const monthNamesFull = ['January','February','March','April','May','June','July',
                        'August','September','October','November','December'];
const weekDays = ['S','M','T','W','T','F','S'];

function createMonthGrid(dateObj){
  const y = dateObj.getFullYear();
  const m = dateObj.getMonth();
  const firstDay   = new Date(y,m,1);
  const startWeekD = firstDay.getDay();                        // 0‑6
  const daysInMon  = new Date(y,m+1,0).getDate();             // 28‑31

  let html = `<div class="flex flex-col gap-2"><div class="font-semibold text-[#232323] text-lg text-center">${monthNamesFull[m]} ${y}</div><div class="grid grid-cols-7 gap-2">`;
  // weekday labels
  weekDays.forEach(d=>{ html += `<div class="font-medium text-gray-400">${d}</div>`; });
  // leading blanks
  for(let b=0;b<startWeekD;b++){ html += '<div></div>'; }
  // days
  for(let d=1; d<=daysInMon; d++){
    const iso = new Date(y,m,d).toISOString().split('T')[0];
    const active = (startDate && iso===startDate) || (endDate && iso===endDate);
    html += `<button class="${active?'selected':''}" data-date="${iso}">${d}</button>`;
  }
  html += '</div></div>';
  return html;
}

function renderCalendar(){
  if(!calGrid) return;
  // compose two consecutive months side‑by‑side
  const secondMonth = new Date(currentMonth.getFullYear(), currentMonth.getMonth()+1, 1);
  calGrid.innerHTML = createMonthGrid(currentMonth) + createMonthGrid(secondMonth);

  // update main label
  calLabel.textContent = `${monthNamesFull[currentMonth.getMonth()]} ${currentMonth.getFullYear()} — ${monthNamesFull[secondMonth.getMonth()]} ${secondMonth.getFullYear()}`;

  // wire up day clicks
  calGrid.querySelectorAll('button[data-date]').forEach(btn=>{
    btn.addEventListener('click',()=>{
      const iso = btn.dataset.date;
      if(!startDate || (startDate && endDate)){
        startDate = iso;
        endDate   = null;
      }else if(new Date(iso) >= new Date(startDate)){
        endDate = iso;
      }else{
        startDate = iso;
        endDate   = null;
      }
      highlightSelection();
    });
  });
  highlightSelection();
}

function highlightSelection(){
  calGrid.querySelectorAll('button[data-date]').forEach(btn=>{
    btn.classList.remove('selected');
    if(btn.dataset.date===startDate || btn.dataset.date===endDate){
      btn.classList.add('selected');
    }
  });
}

window.toggleCalendar = function(){
  if(!calDropdown) return;
  calDropdown.classList.toggle('hidden');
  if(!calDropdown.classList.contains('hidden')) {
    renderCalendar();
  }
}

calPrev?.addEventListener('click',()=>{ currentMonth.setMonth(currentMonth.getMonth()-1); renderCalendar(); });
calNext?.addEventListener('click',()=>{ currentMonth.setMonth(currentMonth.getMonth()+1); renderCalendar(); });
calClear?.addEventListener('click',()=>{
  startDate=null; endDate=null;
  checkInInput.value='Add dates';
  checkOutInput.value='Add dates';
  calDropdown.dataset.start='';
  calDropdown.dataset.end='';
  highlightSelection();
});
calApply?.addEventListener('click',()=>{
  if(startDate){ checkInInput.value = startDate; }
  if(endDate){   checkOutInput.value = endDate; }
  calDropdown.dataset.start=startDate||'';
  calDropdown.dataset.end=endDate||'';
  calDropdown.classList.add('hidden');
});

// close when clicking outside
window.addEventListener('click',e=>{
  if(!calDropdown || calDropdown.classList.contains('hidden')) return;
  if(!calDropdown.contains(e.target) && !checkInInput.contains(e.target) && !checkOutInput.contains(e.target)){
    calDropdown.classList.add('hidden');
  }
});
