#!/bin/bash

list_sinks()
{
  pactl list sink-inputs | awk '/Sink Input #/{ sub(/#/," ");  printf $3" "} /application.icon_name/{ printf $0"\n" }'
}

get_active_app_icon_name()
{
  qdbus org.ayatana.bamf  /org/ayatana/bamf/matcher org.ayatana.bamf.matcher.ActiveApplication \
      | xargs -I {} qdbus org.ayatana.bamf {} org.ayatana.bamf.view.Icon
}



get_sinks_for_app()
{
  list_sinks | while read line ; do

    if grep -q "$APP_ICON_NAME" <<< "$line"
    then
       awk '{printf $1" "}' <<< "$line"
    fi
 done
}

mute_sinks()
{
   for sink_id in $( get_sinks_for_app  ) ; do
       pactl set-sink-input-mute "$sink_id" 1
   done
}

unmute_sinks()

{
   for sink_id in $( get_sinks_for_app  ) ; do
       pactl set-sink-input-mute "$sink_id" 0
   done
}
main()
{
  local APP_ICON_NAME="chromium-browser"

  while true 
  do

     if [ "$( get_active_app_icon_name )" != "$APP_ICON_NAME" ] ;
     then
          mute_sinks
     else 
         unmute_sinks
     fi

  sleep 0.25  
  done
}


main
