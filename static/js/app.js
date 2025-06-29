let whereField, checkinField, checkoutField, whoField;
let searchFields = [];
const checkinIsoInput  = document.getElementById('checkinIso');
const checkoutIsoInput = document.getElementById('checkoutIso');
const guestsTotalInput = document.getElementById('guestsTotal');
function setActiveField(el){
  searchFields.forEach(f => f?.classList.toggle('glass-active', f===el));
}

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

  /* ------- Search bar glass focus ------- */
  whereField    = document.getElementById('whereField');
  checkinField  = document.getElementById('checkinField');
  checkoutField = document.getElementById('checkoutField');
  whoField      = document.getElementById('whoField');
  searchFields  = [whereField, checkinField, checkoutField, whoField];

  const whereInput = document.querySelector('input[name="q"]');
  whereInput?.addEventListener('focus', ()=> setActiveField(whereField));
  whereInput?.addEventListener('blur',  ()=> setActiveField(null));

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
  const whoCounts    = { adults:0, children:0, infants:0, pets:0 };
  if(guestsTotalInput && !guestsTotalInput.value){
    guestsTotalInput.value = 0;
  }

  window.toggleWhoDropdown = function(){
    if(!whoDropdown) return;
    whoDropdown.classList.toggle('hidden');
    setActiveField(whoDropdown.classList.contains('hidden') ? null : whoField);
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
    if(guestsTotalInput){
      guestsTotalInput.value = whoCounts.adults + whoCounts.children + whoCounts.infants;
    }
  }

  // close on click outside
  window.addEventListener('click', e=>{
    if(!whoDropdown || !whoInput) return;
    if(!whoDropdown.contains(e.target) && !whoInput.contains(e.target)){
      whoDropdown.classList.add('hidden');
      setActiveField(null);
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
let calendarField = null; // 'checkin' or 'checkout'

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

  let html = `<div class="flex flex-col gap-2"><div class="font-semibold text-[#232323] text-lg text-center">${monthNamesFull[m]} ${y}</div><div class="grid grid-cols-7 gap-0">`;
  // weekday labels
  weekDays.forEach(d=>{ html += `<div class="font-medium text-gray-400">${d}</div>`; });
  // leading blanks
  for(let b=0;b<startWeekD;b++){ html += '<div></div>'; }
  // days
  for(let d=1; d<=daysInMon; d++){
    const iso = new Date(y,m,d).toISOString().split('T')[0];
    html += `<button type="button" data-date="${iso}">${d}</button>`;
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
    btn.addEventListener('click',(e)=>{
      e.preventDefault();
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
  const start = startDate ? new Date(startDate) : null;
  const end   = endDate ? new Date(endDate) : null;

  calGrid.querySelectorAll('button[data-date]').forEach(btn=>{
    const d = new Date(btn.dataset.date);
    btn.classList.remove('range-start','range-end','in-range','no-after');

    if(start && btn.dataset.date===startDate){
      btn.classList.add('range-start');
      if(!end || start.getTime()===end.getTime()) btn.classList.add('no-after');
    }
    if(end && btn.dataset.date===endDate){
      btn.classList.add('range-end');
      if(!start || start.getTime()===end.getTime()) btn.classList.add('no-after');
    }
    if(start && end && d > start && d < end){
      btn.classList.add('in-range');
    }
  });

  checkInInput.value  = start ? start.toLocaleDateString() : 'Add dates';
  checkOutInput.value = end ? end.toLocaleDateString() : 'Add dates';
  if(checkinIsoInput)  checkinIsoInput.value  = startDate || '';
  if(checkoutIsoInput) checkoutIsoInput.value = endDate || '';
  calDropdown.dataset.start = startDate || '';
  calDropdown.dataset.end   = endDate || '';

  if(start && !end){
    calendarField = 'checkout';
    setActiveField(checkoutField);
  }else if(start && end){
    calendarField = null;
    setActiveField(null);
  }else{
    calendarField = 'checkin';
    setActiveField(checkinField);
  }
}

window.toggleCalendar = function(which){
  if(!calDropdown) return;
  if(which) calendarField = which;
  calDropdown.classList.toggle('hidden');
  if(!calDropdown.classList.contains('hidden')) {
    renderCalendar();
    setActiveField(calendarField==='checkout'?checkoutField:checkinField);
  } else {
    setActiveField(null);
  }
}

calPrev?.addEventListener('click',()=>{ currentMonth.setMonth(currentMonth.getMonth()-1); renderCalendar(); });
calNext?.addEventListener('click',()=>{ currentMonth.setMonth(currentMonth.getMonth()+1); renderCalendar(); });
calClear?.addEventListener('click',()=>{
  startDate = null;
  endDate   = null;
  highlightSelection();
});
calApply?.addEventListener('click',()=>{
  calDropdown.classList.add('hidden');
  setActiveField(null);
});

// close when clicking outside
window.addEventListener('click',e=>{
  if(!calDropdown || calDropdown.classList.contains('hidden')) return;
  if(!calDropdown.contains(e.target) && !checkInInput.contains(e.target) && !checkOutInput.contains(e.target)){
    calDropdown.classList.add('hidden');
    setActiveField(null);
  }
});

/* -------- Property-detail availability calendar -------- */
document.addEventListener('DOMContentLoaded', () => {
  const grid   = document.getElementById('detailCalendarGrid');
  const jsonEl = document.getElementById('bookedDatesJSON');
  if (!grid || !jsonEl) return;                       // not on detail page

  const booked = JSON.parse(jsonEl.textContent || '[]');
  const isBlocked = iso =>
    booked.some(r => iso >= r.start && iso <= r.end);

  let showMonth = new Date(new Date().getFullYear(), new Date().getMonth(), 1);
  let selStart  = null;
  let selEnd    = null;

  const mNames  = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const wNames  = ['S','M','T','W','T','F','S'];

  function monthGrid(dt){
    const y = dt.getFullYear(), m = dt.getMonth();
    const lead = new Date(y,m,1).getDay();
    const days = new Date(y,m+1,0).getDate();
    let html = `<div class="flex flex-col gap-2 flex-1">
      <div class="font-semibold text-lg text-center text-[#232323]">
        ${mNames[m]} ${y}
      </div>
      <div class="grid grid-cols-7 gap-0">`;
    wNames.forEach(d=> html += `<div class="text-xs font-medium text-center text-gray-400">${d}</div>`);
    for(let b=0;b<lead;b++) html += '<div></div>';
    for(let d=1;d<=days;d++){
      const iso = new Date(y,m,d).toISOString().split('T')[0];
      const dis = isBlocked(iso);
      html += `<button data-date="${iso}" ${dis?'disabled':''}
               class="h-14 w-14 flex items-center justify-center rounded text-[#232323] text-base
               ${dis?'opacity-30 cursor-not-allowed':'hover:bg-[#F8ECD8]'}">
               ${d}</button>`;
    }
    html += '</div></div>';
    return html;
  }

  function render(){
    const next = new Date(showMonth.getFullYear(), showMonth.getMonth()+1, 1);
    grid.innerHTML = monthGrid(showMonth) + monthGrid(next);
    highlight();
  }

  function highlight(){
    grid.querySelectorAll('button[data-date]').forEach(b=>{
      const iso = b.dataset.date;
      b.classList.remove('range-start','range-end','in-range','no-after');
      b.classList.remove('bg-gold','text-white','bg-[#F8ECD8]');

      if(selStart && iso===selStart){
        b.classList.add('range-start','bg-gold','text-white');
        if(!selEnd || selStart===selEnd) b.classList.add('no-after');
      }
      if(selEnd && iso===selEnd){
        b.classList.add('range-end','bg-gold','text-white');
        if(!selStart || selStart===selEnd) b.classList.add('no-after');
      }
      if(selStart && selEnd && iso>selStart && iso<selEnd){
        b.classList.add('in-range','bg-[#F8ECD8]');
      }
    });

    document.getElementById('detailSelected').textContent =
      selStart && selEnd ? `${selStart} – ${selEnd}` : '';
  }

  grid.addEventListener('click', e => {
    const btn = e.target.closest('button[data-date]');
    if (!btn || btn.disabled) return;
    const iso = btn.dataset.date;
    if (!selStart || (selStart && selEnd)) {
      // no start chosen or full range already selected
      selStart = iso;
      selEnd = null;
    } else if (selStart && !selEnd) {
      // choosing an end date or restarting start earlier in time
      if (new Date(iso) >= new Date(selStart)) {
        selEnd = iso;
      } else {
        selStart = iso;
      }
    }
    highlight();
  });

  document.getElementById('detailClear')?.addEventListener('click', ()=>{
    selStart = selEnd = null; highlight();
  });

  render();
});
