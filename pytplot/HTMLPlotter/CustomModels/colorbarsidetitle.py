# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from bokeh.models.annotations import ColorBar
from bokeh.util.compiler import TypeScript

ts_code = '''
import {ColorBar, ColorBarView} from "models/annotations/color_bar"
import * as p from "core/properties"
import {Context2d} from "core/util/canvas"

const SHORT_DIM = 25

export class ColorBarSideTitleView extends ColorBarView {
  model: ColorBarSideTitle
  protected image: HTMLCanvasElement

  compute_legend_dimensions(): {width: number, height: number} {
    const image_dimensions = this._computed_image_dimensions()
    const [image_height, image_width] = [image_dimensions.height, image_dimensions.width]

    const label_extent = this._get_label_extent()
    const title_extent = this._title_extent()
    const tick_extent = this._tick_extent()
    const {padding} = this.model

    let legend_height: number, legend_width: number
    legend_height = image_height
    legend_width = image_width + tick_extent + label_extent + title_extent + 2*padding

    return {width: legend_width, height: legend_height}
  }

  protected _draw_image(ctx: Context2d): void {
    const image = this._computed_image_dimensions()
    ctx.save()
    ctx.setImageSmoothingEnabled(false)
    ctx.globalAlpha = this.model.scale_alpha
    ctx.drawImage(this.image, 0, 0, image.width, image.height)
    if (this.visuals.bar_line.doit) {
      this.visuals.bar_line.set_value(ctx)
      ctx.strokeRect(0, 0, image.width, image.height)
    }
    ctx.restore()
  }

  protected _draw_title(ctx: Context2d): void {
    if (!this.visuals.title_text.doit)
      return
    const label_extent = this._get_label_extent()
    const tick_extent = this._tick_extent()
    const {padding} = this.model
    ctx.save()
    this.visuals.title_text.set_value(ctx)
    ctx.rotate(-Math.PI/2)
    ctx.fillText(this.model.title, -this.plot_view.frame._height.value * 0.5 , this.image.width + tick_extent + label_extent + 4*padding)
    ctx.textAlign="center"
    ctx.restore()
  }

  /*protected*/ _get_image_offset(): {x: number, y: number} {
    // Returns image offset relative to legend bounding box
    const x = this.model.padding
    const y = 0
    return {x, y}
  }

  _computed_image_dimensions(): {height: number, width: number} {
    const frame_height = this.plot_view.frame._height.value
    let height: number, width: number
    if (this.model.height == 'auto') {
        height = frame_height
    } else
    height = this.model.height

    width = this.model.width == 'auto' ? SHORT_DIM : this.model.width

    return {width, height}
  }

  // }}}
}

export namespace ColorBarSideTitle {
  export type Attrs = p.AttrsOf<Props>

  export type Props = ColorBar.Props
}

export interface ColorBarSideTitle extends ColorBarSideTitle.Attrs {}

export class ColorBarSideTitle extends ColorBar {
  properties: ColorBarSideTitle.Props
  
  constructor(attrs?: Partial<ColorBarSideTitle.Attrs>) {
    super(attrs)
  }

  static initClass(): void {
    this.prototype.default_view = ColorBarSideTitleView
  }
}

ColorBarSideTitle.initClass()

'''


class ColorBarSideTitle(ColorBar):
    __implementation__ = TypeScript(ts_code)