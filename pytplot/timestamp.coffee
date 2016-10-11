_ = require "underscore"
$ = require "jquery"

p = require "core/properties"

LayoutDOM = require "models/layouts/layout_dom"

class TimeStampView extends LayoutDOM.View

	initialize: (options) ->
		super(options)
		
		@render()
		
	render: () ->
		@$el.html("<p>#{ @model.text }</p>")
		@$('p').css({ 'width': '800px', 'word-spacing': '683px', 'font-size': '11px', 'color': '#000000', 'background-color': '#ffffff' })

class TimeStamp extends LayoutDOM.Model

	default_view: TimeStampView
	
	type: "TimeStamp"
	
	@define {
		text: [ p.String ]
	}

module.exports =
	Model: TimeStamp
	View: TimeStampView	