<?php

/**
 *
 * bareos-webui - Bareos Web-Frontend
 *
 * @link      https://github.com/bareos/bareos-webui for the canonical source repository
 * @copyright Copyright (c) 2013-2016 Bareos GmbH & Co. KG (http://www.bareos.org/)
 * @license   GNU Affero General Public License (http://www.gnu.org/licenses/)
 * @author    Tobias Ehrig
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 */
namespace Application\View\Helper;

use Zend\View\Helper\AbstractHelper;

class FormatBytes extends AbstractHelper
{

   /**
    * 
    * @param integer $bytes
    * @param boolean $force_unit
    * @param boolean $format
    * @param boolean $si
    * @return string
    */
   public function __invoke($bytes, $force_unit = null, $format = null, $si = true)
   {
      $format = ($format === null) ? '%01.2f %s' : (string) $format;
      if ($si == false OR strpos($force_unit, 'i') !== false) {
         $units = array('B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB');
         $mod   = 1024;
      } else {
         $units = array('B', 'kB', 'MB', 'GB', 'TB', 'PB');
         $mod   = 1000;
      }
      if (($power = array_search((string) $force_unit, $units)) === false) {
         $power = ($bytes > 0) ? floor(log($bytes, $mod)) : 0;
      }
      return sprintf($format, $bytes / pow($mod, $power), $units[$power]);
   }
}

