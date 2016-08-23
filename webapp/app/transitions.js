export default function() {
    this.transition(
	this.hasClass('slide'),
	this.toValue(true),
	this.use('toRight'),
	this.reverse('toLeft')
    );

    this.transition(
	this.hasClass('collapse-up'),
	this.toValue(true),
	this.use('toUp'),
	this.reverse('toDown')
    );

}
