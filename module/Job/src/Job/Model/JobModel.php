<?php

/**
 *
 * bareos-webui - Bareos Web-Frontend
 *
 * @link      https://github.com/bareos/bareos-webui for the canonical source repository
 * @copyright Copyright (c) 2013-2016 Bareos GmbH & Co. KG (http://www.bareos.org/)
 * @license   GNU Affero General Public License (http://www.gnu.org/licenses/)
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

namespace Job\Model;

class JobModel
{
   public function getJobs(&$bsock=null, $jobname=null, $days=null)
   {
      if(isset($bsock)) {
         if($days == "all") {
            if($jobname == "all") {
               $cmd = 'llist jobs';
            }
            else {
               $cmd = 'llist jobs jobname="'.$jobname.'"';
            }
         }
         else  {
            if($jobname == "all") {
               $cmd = 'llist jobs days='.$days;
            }
            else {
               $cmd = 'llist jobs jobname="'.$jobname.'" days='.$days;
            }
         }
         $result = $bsock->send_command($cmd, 2, null);
         if(preg_match('/Failed to send result as json. Maybe result message to long?/', $result)) {
            //return false;
            $error = \Zend\Json\Json::decode($result, \Zend\Json\Json::TYPE_ARRAY);
            return $error['result']['error'];
         }
         else {
            $jobs = \Zend\Json\Json::decode($result, \Zend\Json\Json::TYPE_ARRAY);
            return $jobs['result']['jobs'];
         }
      }
      else {
         throw new \Exception('Missing argument.');
      }
   }

   public function getJobsByStatus(&$bsock=null, $jobname=null, $status=null, $days=null, $hours=null)
   {
      if(isset($bsock, $status)) {
         if(isset($days)) {
            if($days == "all") {
               $cmd = 'llist jobs jobstatus='.$status.'';
            }
            else {
               $cmd = 'llist jobs jobstatus='.$status.' days='.$days.'';
            }
         }
         elseif(isset($hours)) {
            if($hours == "all") {
               $cmd = 'llist jobs jobstatus='.$status.'';
            }
            else {
               $cmd = 'llist jobs jobstatus='.$status.' hours='.$hours.'';
            }
         }
         else {
            $cmd = 'llist jobs jobstatus='.$status.'';
         }
         if($jobname != "all") {
            $cmd .= ' jobname="'.$jobname.'"';
         }
         $result = $bsock->send_command($cmd, 2, null);
         $jobs = \Zend\Json\Json::decode($result, \Zend\Json\Json::TYPE_ARRAY);
         return array_reverse($jobs['result']['jobs']);
      }
      else {
         throw new \Exception('Missing argument.');
      }
   }

   public function getJob(&$bsock=null, $id=null)
   {
      if(isset($bsock, $id)) {
         $cmd = 'llist jobid='.$id.'';
         $result = $bsock->send_command($cmd, 2, null);
         $job = \Zend\Json\Json::decode($result, \Zend\Json\Json::TYPE_ARRAY);
         return $job['result']['jobs'];
      }
      else {
         throw new \Exception('Missing argument.');
      }
   }

   public function getJobLog(&$bsock=null, $id=null)
   {
      if(isset($bsock, $id)) {
         $cmd = 'list joblog jobid='.$id.'';
         $result = $bsock->send_command($cmd, 2, null);
         if(preg_match('/Failed to send result as json. Maybe result message to long?/', $result)) {
            //return false;
            $error = \Zend\Json\Json::decode($result, \Zend\Json\Json::TYPE_ARRAY);
            return $error['result']['error'];
         }
         else {
            $log = \Zend\Json\Json::decode($result, \Zend\Json\Json::TYPE_ARRAY);
            return $log['result']['joblog'];
         }

      }
      else {
         throw new \Exception('Missing argument.');
      }
   }

   public function getJobsByType(&$bsock=null, $type=null)
   {
      if(isset($bsock)) {
         if($type == null) {
            $cmd = '.jobs';
         }
         else {
            $cmd = '.jobs type="'.$type.'"';
         }
         $result = $bsock->send_command($cmd, 2, null);
         $jobs = \Zend\Json\Json::decode($result, \Zend\Json\Json::TYPE_ARRAY);
         return $jobs['result']['jobs'];
      }
      else {
         throw new \Exception('Missing argument.');
      }
   }

   public function getJobsLastStatus(&$bsock=null)
   {
      if(isset($bsock)) {
         $cmd = 'llist jobs last current enabled';
         $result = $bsock->send_command($cmd, 2, null);
         $jobs = \Zend\Json\Json::decode($result, \Zend\Json\Json::TYPE_ARRAY);
         return $jobs['result']['jobs'];
      }
      else {
         throw new \Exception('Missing argument.');
      }
   }
   
   public function getRunningJobStatus(&$bsock = null, $jobid = null)
   {
       if(!isset($bsock)) {
           throw new \Exception('Missing argument.');
       }
       $values = [];
        
       if (is_null($jobid)) {
           $runningJobs = $this->getJobsByStatus($bsock, null, 'R');
       } else {
           $runningJobs[] = ['jobid' => $jobid];
       }
        
       foreach ($runningJobs as $job) {
            
           $cmd = 'status jobid=' . $job['jobid'];
           $result = $bsock->send_command($cmd, 0, null);
            
           // Match lines
           $regex = 'Writing:\s(.+)\sBackup\sjob\s(.+)\sJobId=([\d]+)\sVolume="(.+)"\n(.*)\n(.*)\n\s+Files=([\d,]+)\sBytes=([\d,]+)\sAveBytes\/sec=([\d,]+)\sLastBytes\/sec=([\d,]+)\s';
            
           $values[$job['jobid']] = [];
           $matches = [];
            
           if (preg_match_all('/' . $regex . '/', $result, $matches, PREG_SET_ORDER)) {
               foreach ($matches as $job) {
                   $tmpJobId = $job[3];
                   $values[$tmpJobId]['type']   = $job[1];
                   $values[$tmpJobId]['client'] = $job[2];
                   $values[$tmpJobId]['volume'] = $job[4];
                   $values[$tmpJobId]['files']  = str_replace(",", "", $job[7]);
                   $values[$tmpJobId]['bytes']  = str_replace(",", "", $job[8]);
                   $values[$tmpJobId]['avgbytes_sec']  = str_replace(",", "", $job[9]);
                   $values[$tmpJobId]['lastbytes_sec']  = str_replace(",", "", $job[10]);
                    
                   if (!is_null($jobid) && $jobid == $job[3]) {
                       return $values[$tmpJobId];
                   }
               }
           }
       }
       return $values;
   }

   public function getRestoreJobs(&$bsock=null)
   {
      if(isset($bsock)) {
         $cmd = '.jobs type=R';
         $result = $bsock->send_command($cmd, 2, null);
         $restorejobs = \Zend\Json\Json::decode($result, \Zend\Json\Json::TYPE_ARRAY);
         return $restorejobs['result']['jobs'];
      }
      else {
         throw new \Exception('Missing argument.');
      }
   }

   public function runJob(&$bsock=null, $name=null)
   {
      if(isset($bsock, $name)) {
         $cmd = 'run job="'.$name.'" yes';
         $result = $bsock->send_command($cmd, 0, null);
         return $result;
      }
      else {
         throw new \Exception('Missing argument.');
      }
   }

   public function rerunJob(&$bsock=null, $id=null)
   {
      if(isset($bsock, $id)) {
         $cmd = 'rerun jobid='.$id.' yes';
         $result = $bsock->send_command($cmd, 0, null);
         return $result;
      }
      else {
         throw new \Exception('Missing argument.');
      }
   }

   public function cancelJob(&$bsock=null, $id=null)
   {
      if(isset($bsock, $id)) {
         $cmd = 'cancel jobid='.$id.' yes';
         $result = $bsock->send_command($cmd, 0, null);
         return $result;
      }
      else {
         throw new \Exception('Missing argument.');
      }
   }

   public function enableJob(&$bsock=null, $name=null)
   {
      if(isset($bsock, $name)) {
         $cmd = 'enable job="'.$name.'" yes';
         $result = $bsock->send_command($cmd, 0, null);
         return $result;
      }
      else {
         throw new \Exception('Missing argument.');
      }
   }

   public function disableJob(&$bsock=null, $name=null)
   {
      if(isset($bsock, $name)) {
         $cmd = 'disable job="'.$name.'" yes';
         $result = $bsock->send_command($cmd, 0, null);
         return $result;
      }
      else {
         throw new \Exception('Missing argument.');
      }
   }
}
