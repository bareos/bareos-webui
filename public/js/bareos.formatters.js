function formatBytesExt(bytes, si = true, force_unit = null)
{
	var format = (format == null) ? '%01.2f %s' : format;
	var force_unit = (force_unit == null) ? false : (force_unit.indexOf('i') ? si = true : '');
	
	if (si == false) {
		var units = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB'];
		var mod   = 1024;
	} else {
	   var units = ['B', 'kB', 'MB', 'GB', 'TB', 'PB'];
	   var mod   = 1000;
	}
	
	var i = Math.floor(Math.log(bytes) / Math.log(mod));
	return parseFloat(bytes / Math.pow(mod, i)).toFixed(2)  + ' ' + units[i];
}