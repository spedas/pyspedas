# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

from bokeh.core.properties import String
from bokeh.models import LayoutDOM
from bokeh.util.compiler import TypeScript

JS_CODE = '''
import * as p from "core/properties"
import {div, empty} from "core/dom"
import {LayoutDOM, LayoutDOMView} from "models/layouts/layout_dom"
import {LayoutItem} from "core/layout"

export class TimeStampView extends LayoutDOMView {
    model: TimeStamp
    
    initialize(): void {
        super.initialize()
    }
    render(): void {
        empty(this.el)
        this.el.appendChild(div({
          style: {
            'width': '800px',
            'word-spacing': '10px',
            'font-size': '11px',
            'color': '#000000',
            'background-color': '#ffffff',
            },
        }, `${this.model.text}`))
    }
    
    _update_layout(): void {
        this.layout = new LayoutItem()
        this.layout.set_sizing(this.box_sizing())
    }
    
    get child_models(): LayoutDOM[] {
        return []
      }
}


export namespace TimeStamp {
  export type Attrs = p.AttrsOf<Props>

  export type Props = LayoutDOM.Props & {
    text: p.Property<string>
  }
}

export interface TimeStamp extends TimeStamp.Attrs {}

export class TimeStamp extends LayoutDOM {
    properties: TimeStamp.Props
    static initClass(): void {
    
        this.prototype.default_view = TimeStampView
    
        this.define<TimeStamp.Props>({
            text: [ p.String ]
        })
    }
}

TimeStamp.initClass()

'''


class TimeStamp(LayoutDOM):
    __implementation__ = TypeScript(JS_CODE)
    text = String(default = "Testing")

