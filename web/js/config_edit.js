document.addEventListener('contextmenu', event => event.preventDefault());
async function main() {
  var current_vm = await eel.get_vm_name()();
  var config = await eel.get_config()();
  var save = document.getElementById('save');
  var no_save = document.getElementById('no_save');
  document.title = "Edit " + current_vm + " - Pixelsuft DosBox VM";
  window.addEventListener('resize', function() {
    if (window.innerHeight < 480) window.resizeTo(window.outerWidth, 480);
    if (window.innerWidth < 640) window.resizeTo(640, window.outerHeight);
  });
  no_save.addEventListener('click', function() {
    location.href = "/";
  });
  if (config !== false) {
    if (config[0] == 'true') document.getElementById('fullscreen').checked = true;
    document.getElementById('fullresolution').value = config[1];
    document.getElementById('windowresolution').value = config[2];
    document.getElementById('output').value = config[3];
    document.getElementById('sensitivity').value = parseInt(config[4]);
    document.getElementById('language').value = config[5];
    document.getElementById('machine').value = config[6];
    document.getElementById('memsize').value = parseInt(config[7]);
    document.getElementById('core').value = config[8];
    document.getElementById('cputype').value = config[9];
    document.getElementById('cycles').value = config[10];
    console.log(config[11]);
    if (config[11] == 'true') document.getElementById('xms').checked = true;
    if (config[12] == 'true') document.getElementById('ems').checked = true;
    if (config[13] == 'true') document.getElementById('umb').checked = true;
    document.getElementById('keyboardlayout').value = config[14];
    document.getElementById('fda').value = config[15];
    document.getElementById('fdb').value = config[16];
    document.getElementById('hda').value = config[17];
    document.getElementById('hdb').value = config[18];
    document.getElementById('hda_g').value = config[19];
    document.getElementById('hdb_g').value = config[20];
    document.getElementById('mount_a').value = config[21];
    document.getElementById('mount_c').value = config[22];
  }
  save.addEventListener('click', async function() {
    var cfg = [
      document.getElementById('fullscreen').checked,
      document.getElementById('fullresolution').value,
      document.getElementById('windowresolution').value,
      document.getElementById('output').value,
      document.getElementById('sensitivity').value,
      document.getElementById('language').value,
      document.getElementById('machine').value,
      document.getElementById('memsize').value,
      document.getElementById('core').value,
      document.getElementById('cputype').value,
      document.getElementById('cycles').value,
      document.getElementById('xms').checked,
      document.getElementById('ems').checked,
      document.getElementById('umb').checked,
      document.getElementById('keyboardlayout').value,
      document.getElementById('fda').value,
      document.getElementById('fdb').value,
      document.getElementById('hda').value,
      document.getElementById('hdb').value,
      document.getElementById('hda_g').value,
      document.getElementById('hdb_g').value,
      document.getElementById('mount_a').value,
      document.getElementById('mount_c').value
    ];
    if (await eel.save_config(cfg)() == true) location.href = "/";
  });
}
main();
