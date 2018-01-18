# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from bokeh.core.properties import String
from bokeh.models.annotations import ColorBar
#from bokeh.core.properties import String, Instance
#from bokeh.models import LayoutDOM, Slider

#This is the start of a future implementation of JS_CODE
#when bokeh moves to typescript.  Please ignore for now.  
JS_CODE2 = '''
import {min, max, range} from "core/util/array"
 
import {ColorBar, ColorBarView} from "models/annotations/color_bar"
import {isEmpty} from "core/util/object"

SHORT_DIM = 25
LONG_DIM_MIN_SCALAR = 0.3
LONG_DIM_MAX_SCALAR = 0.8
export class ColorBarSideTitleView extends ColorBarView
 
  compute_legend_dimensions () {
    let legend_height, legend_width;
    const image_dimensions = this.model._computed_image_dimensions();
    const [image_height, image_width] = [image_dimensions.height, image_dimensions.width];
 
    const label_extent = this._get_label_extent();
    const title_extent = this.model._title_extent();
    const tick_extent = this.model._tick_extent();
    const { padding } = this.model.padding;
 
    switch (this.model.orientation) {
      case "vertical":
        legend_height = image_height;
        legend_width = image_width + tick_extent + title_extent + label_extent + (padding * 2);
        break;
      case "horizontal":
        legend_height = image_height + tick_extent + label_extent + (padding * 2);
        legend_width = image_width + title_extent + (padding * 2);
        break;
    }
    
    return {height: legend_height, width: legend_width}
   
  }
   
  render() {
    if (!this.model.visible || (this.model.color_mapper == null)) {
      return
    }
    const { ctx } = this.plot_view.canvas_view;
    ctx.save()
 
    const {sx, sy} = this.compute_legend_location();
    ctx.translate(location.sx, location.sy);
    this._draw_bbox(ctx);
 
    const image_offset = this._get_image_offset();
    ctx.translate(image_offset.x, image_offset.y);
 
    this._draw_image(ctx);
 
    if ((this.model.color_mapper.low != null) && (this.model.color_mapper.high != null)) {
      const tick_info = this.model.tick_info();
      this._draw_major_ticks(ctx, tick_info);
      this._draw_minor_ticks(ctx, tick_info);
      this._draw_major_labels(ctx, tick_info);
 
    if (this.model.title) {
      this._draw_title(ctx);
    }
    ctx.restore()
  }
 
  _draw_title: (ctx) ->
    if not @visuals.title_text.doit
      return
    image = @compute_legend_dimensions()
    ctx.save()
    @visuals.title_text.set_value(ctx)
    ctx.rotate(-Math.PI/2)
    ctx.textAlign="center"
    ctx.fillText(@model.title, -image.height * 0.5, image.width-@model._title_extent())
    ctx.restore()
 
  _get_image_offset: () ->
    # Returns image offset relative to legend bounding box
    x = @model.padding
    y = 0
    return {x: x, y: y}
 
  _get_label_extent: () ->
    major_labels = @model.tick_info().labels.major
    if @model.color_mapper.low? and @model.color_mapper.high? and not isEmpty(major_labels)
      ctx = @plot_view.canvas_view.ctx
      ctx.save()
      @visuals.major_label_text.set_value(ctx)
 
      switch @model.orientation
        when "vertical"
          label_extent = max((ctx.measureText(label.toString()).width for label in major_labels))
        when "horizontal"
          label_extent = text_util.get_text_height(@visuals.major_label_text.font_value()).height
 
      label_extent += @model.label_standoff
      ctx.restore()
    else
      label_extent = 0
    return label_extent
 
export class ColorBarSideTitle extends ColorBar
  default_view: ColorBarSideTitleView
  type: 'ColorBarSideTitle'
 
  _computed_image_dimensions: () ->
    ###
    Heuristics to determine ColorBar image dimensions if set to "auto"
    Note: Returns the height/width values for the ColorBar's scale image, not
    the dimensions of the entire ColorBar.
    If the short dimension (the width of a vertical bar or height of a
    horizontal bar) is set to "auto", the resulting dimension will be set to
    25 px.
    For a ColorBar in a side panel with the long dimension (the height of a
    vertical bar or width of a horizontal bar) set to "auto", the
    resulting dimension will be as long as the adjacent frame edge, so that the
    bar "fits" to the plot.
    For a ColorBar in the plot frame with the long dimension set to "auto", the
    resulting dimension will be the greater of:
      * The length of the color palette * 25px
      * The parallel frame dimension * 0.30
        (i.e the frame height for a vertical ColorBar)
    But not greater than:
      * The parallel frame dimension * 0.80
    ###

    frame_height = @plot.plot_canvas.frame._height.value
    frame_width = @plot.plot_canvas.frame._width.value
    title_extent = 0

    switch @orientation
      when "vertical"
        if @height == 'auto'
          if @panel?
            height = frame_height
          else
            height = max([@color_mapper.palette.length * SHORT_DIM,
                            frame_height * LONG_DIM_MIN_SCALAR])
            height = min([height,
                            frame_height * LONG_DIM_MAX_SCALAR - 2 * @padding - title_extent])
        else
          height = @height
 
        width = if @width == 'auto' then SHORT_DIM else @width

      when "horizontal"
        height = if @height == 'auto' then SHORT_DIM else @height
 
        if @width == 'auto'
          if @panel?
            width = frame_width
          else
            width = max([@color_mapper.palette.length * SHORT_DIM,
                           frame_width * LONG_DIM_MIN_SCALAR])
            width = min([width,
                           frame_width * LONG_DIM_MAX_SCALAR - 2 * @padding])
        else
          width = @width

    return {"height": height, "width": width}
     
 
 
'''

JS_CODE = '''
import {min, max} from "core/util/array"
 
import {ColorBar, ColorBarView} from "models/annotations/color_bar"
import {isEmpty} from "core/util/object"

SHORT_DIM = 25
LONG_DIM_MIN_SCALAR = 0.3
LONG_DIM_MAX_SCALAR = 0.8
export class ColorBarSideTitleView extends ColorBarView
 
  compute_legend_dimensions: () ->
    image_dimensions = @model._computed_image_dimensions()
    [image_height, image_width] = [image_dimensions.height, image_dimensions.width]
 
    label_extent = @_get_label_extent()
    title_extent = @model._title_extent()
    tick_extent = @model._tick_extent()
    padding = @model.padding
 
    switch @model.orientation 
      when "vertical"
        legend_height = image_height
        legend_width = image_width + tick_extent + title_extent + label_extent + (padding * 2)
        break
      when "horizontal"
        legend_height = image_height + tick_extent + label_extent + (padding * 2)
        legend_width = image_width + title_extent + (padding * 2)
        break
    
    
    return {height: legend_height, width: legend_width}
   
   
  render: () -> 
    if not @model.visible or not @model.color_mapper?
      return

    ctx = @plot_view.canvas_view.ctx
    ctx.save()
 
    {sx, sy} = @compute_legend_location()
    ctx.translate(sx, sy)
    @_draw_bbox(ctx)
 
    image_offset = @_get_image_offset()
    ctx.translate(image_offset.x, image_offset.y)
 
    @_draw_image(ctx)
 
    if @model.color_mapper.low? and @model.color_mapper.high?
      tick_info = @model.tick_info()
      @_draw_major_ticks(ctx, tick_info)
      @_draw_minor_ticks(ctx, tick_info)
      @_draw_major_labels(ctx, tick_info)

    if @model.title
      @_draw_title(ctx)
    ctx.restore()
 
  _draw_title: (ctx) ->
    if not @visuals.title_text.doit
      return
    image = @compute_legend_dimensions()
    ctx.save()
    @visuals.title_text.set_value(ctx)
    ctx.rotate(-Math.PI/2)
    ctx.textAlign="center"
    ctx.fillText(@model.title, -image.height * 0.5, image.width-@model._title_extent())
    ctx.restore()
 
  _get_image_offset: () ->
    # Returns image offset relative to legend bounding box
    x = @model.padding
    y = 0
    return {x: x, y: y}
 
  _get_label_extent: () ->
    major_labels = @model.tick_info().labels.major
    if @model.color_mapper.low? and @model.color_mapper.high? and not isEmpty(major_labels)
      ctx = @plot_view.canvas_view.ctx
      ctx.save()
      @visuals.major_label_text.set_value(ctx)
 
      switch @model.orientation
        when "vertical"
          label_extent = max((ctx.measureText(label.toString()).width for label in major_labels))
        when "horizontal"
          label_extent = text_util.get_text_height(@visuals.major_label_text.font_value()).height
 
      label_extent += @model.label_standoff
      ctx.restore()
    else
      label_extent = 0
    return label_extent
 
export class ColorBarSideTitle extends ColorBar
  default_view: ColorBarSideTitleView
  type: 'ColorBarSideTitle'
 
  _computed_image_dimensions: () ->
    ###
    Heuristics to determine ColorBar image dimensions if set to "auto"
    Note: Returns the height/width values for the ColorBar's scale image, not
    the dimensions of the entire ColorBar.
    If the short dimension (the width of a vertical bar or height of a
    horizontal bar) is set to "auto", the resulting dimension will be set to
    25 px.
    For a ColorBar in a side panel with the long dimension (the height of a
    vertical bar or width of a horizontal bar) set to "auto", the
    resulting dimension will be as long as the adjacent frame edge, so that the
    bar "fits" to the plot.
    For a ColorBar in the plot frame with the long dimension set to "auto", the
    resulting dimension will be the greater of:
      * The length of the color palette * 25px
      * The parallel frame dimension * 0.30
        (i.e the frame height for a vertical ColorBar)
    But not greater than:
      * The parallel frame dimension * 0.80
    ###

    frame_height = @plot.plot_canvas.frame._height.value
    frame_width = @plot.plot_canvas.frame._width.value
    title_extent = 0

    switch @orientation
      when "vertical"
        if @height == 'auto'
          if @panel?
            height = frame_height
          else
            height = max([@color_mapper.palette.length * SHORT_DIM,
                            frame_height * LONG_DIM_MIN_SCALAR])
            height = min([height,
                            frame_height * LONG_DIM_MAX_SCALAR - 2 * @padding - title_extent])
        else
          height = @height
 
        width = if @width == 'auto' then SHORT_DIM else @width

      when "horizontal"
        height = if @height == 'auto' then SHORT_DIM else @height
 
        if @width == 'auto'
          if @panel?
            width = frame_width
          else
            width = max([@color_mapper.palette.length * SHORT_DIM,
                           frame_width * LONG_DIM_MIN_SCALAR])
            width = min([width,
                           frame_width * LONG_DIM_MAX_SCALAR - 2 * @padding])
        else
          width = @width

    return {"height": height, "width": width}
     
 
 
'''
class ColorBarSideTitle(ColorBar):
    #__javascript__ = ["https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/underscore-min.js"]
    __implementation__ = JS_CODE 