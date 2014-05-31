#!/bin/env bash

RAW_FOLDER=.
WATERMARKED_FOLDER=.
THUMBS_FOLDER=.

for file in $RAW_FOLDER/test1.jpg
do
    echo "generating watermark for $file"
    # next line checks the mime-type of the file
    IMAGE_TYPE=`file --mime-type -b "$file" | awk -F'/' '{print $1}'`
    echo "  image type: $IMAGE_TYPE"
    if [ x$IMAGE_TYPE = "ximage" ]; then
        IMAGE_SIZE=`identify -format "%wx%h" $file`
        #`file -b $file | sed 's/ //g' | sed 's/,/ /g' | awk  '{print $2}'`
        WIDTH=`echo $IMAGE_SIZE | sed 's/x/ /g' | awk '{print $1}'`
        HEIGHT=`echo $IMAGE_SIZE | sed 's/x/ /g' | awk '{print $2}'`  
        echo "  size: $IMAGE_SIZE, width: $WIDTH, height: $HEIGHT"
        filename=$(basename "$file")
        extension="${filename##*.}"
        filename="${filename%.*}"
        
        WATERMARK_IMG="$filename-watermark.png"

         #create trans img w watermark with custom size
        S_W=4
        S_H=20
        W=$((WIDTH - $((WIDTH/S_W))))
        H=$((HEIGHT - $((HEIGHT/S_H))))
        echo "  mark location: $W, $H"
        convert -size "$WIDTH"x"$HEIGHT" xc:transparent -font Courier-bold -pointsize 25 -fill SlateBlue1 -draw "text $W,$H 'octavian g'" "$WATERMARK_IMG"
        
        echo "  watermark: $WATERMARK_IMG"
        
        
        composite -dissolve 50% -quality 100 "$WATERMARK_IMG" "$file" "${WATERMARKED_FOLDER}/${filename}_marked.${extension}"  
        echo "  watermarked image output: ${WATERMARKED_FOLDER}/${filename}_marked.${extension}"
    fi 
done

for file in $WATERMARKED_FOLDER/test1_marked.jpg
do
    echo "generating thumb for $file"
    # next line checks the mime-type of the file
    IMAGE_TYPE=`file --mime-type -b "$file" | awk -F'/' '{print $1}'`
    echo "image type: $IMAGE_TYPE"
    if [ x$IMAGE_TYPE = "ximage" ]; then
        IMAGE_SIZE=`identify -format "%wx%h" $file`
        #`file -b $file | sed 's/ //g' | sed 's/,/ /g' | awk  '{print $2}'`
        WIDTH=`echo $IMAGE_SIZE | sed 's/x/ /g' | awk '{print $1}'`
        HEIGHT=`echo $IMAGE_SIZE | sed 's/x/ /g' | awk '{print $2}'`  
        echo "size: $IMAGE_SIZE, width: $WIDTH, height: $HEIGHT"
        
        # If the image width is greater that 200 or the height is greater that 150 a thumb is created
        #if [ $WIDTH -ge  201 ] || [ $HEIGHT -ge 151 ]; then
        #This line convert the image in a 200 x 150 thumb 
        filename=$(basename "$file")
        extension="${filename##*.}"
        filename="${filename%.*}"
        
        #generate thumbnail:
        convert -sample 200x150 "$file" "${THUMBS_FOLDER}/${filename}_thumb.${extension}"  
        
        
        #fi
    fi     
done
