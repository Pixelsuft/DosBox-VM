document.addEventListener('contextmenu', event => event.preventDefault());
async function main(){
  var spisok = document.getElementById('spisok');
  var selected_vm = document.getElementById('selected_vm');
  var vm_list = await eel.get_all_vms()();
  var plus = document.getElementById('plus');
  var minus = document.getElementById('minus');
  var run = document.getElementById('run');
  var sets = document.getElementById('sets');


  for(var i=0;i<vm_list.length;i++){
    spisok.innerHTML += '\n<option value="' + vm_list[i] + '">' + vm_list[i] + '</option>';
    spisok.size += 1;
  }
  if(spisok.size < 2)spisok.size = 2;
  if(vm_list.length > 0)
  {
    selected_vm.value=vm_list[0];
    await eel.set_current_vm(vm_list[0])();
  }

  async function on_vm_change(){
    selected_vm.value = spisok.value;
    await eel.set_current_vm(spisok.value)();
  }
  plus.addEventListener('click', async function(){
    if(await eel.add_new_vm(selected_vm.value)() == true){
      location.reload();
    }
  });
  minus.addEventListener('click', async function(){
    if(await eel.remove_old_vm(selected_vm.value)() == true){
      location.reload();
    }
  });
  run.addEventListener('click', async function(){
    await eel.run_vm(selected_vm.value)();
  });
  sets.addEventListener('click', function(){
    if(true){
      location.href = "config_edit.html";
    }
  });
  window.addEventListener('resize', function(){
    if(window.innerHeight < 480)window.resizeTo(window.outerWidth, 480);
    if(window.innerWidth < 640)window.resizeTo(640, window.outerHeight);
  });
  spisok.addEventListener('change', on_vm_change);
  spisok.addEventListener('click', on_vm_change);
}
main();
