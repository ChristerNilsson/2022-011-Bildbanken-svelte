<script>
	const helpTexts = []
	helpTexts.push("Separate words with a space or an underscore (_)")
	helpTexts.push("Search is case sensitive")
	helpTexts.push("Searching can start anywhere in a word")
	helpTexts.push("Number in parenthesis is number of images found")
	helpTexts.push("Search period like 2022-09-17, 2022-09, 2022 or 09-17")
	helpTexts.push("Search Tournament numbers like T10370")
	helpTexts.push("Search Member numbers like M585772")
	helpTexts.push("[None] unmarks images")
	helpTexts.push("[Download] zips marked images")
	helpTexts.push("[All] marks images")
	helpTexts.push("Home is the highest level directory")
	helpTexts.push("Ancestors are shown to the left of the Current directory")
	helpTexts.push("[Up] sets the Current directory to the closest ancestor")
	helpTexts.push("Directory selection is similar to Explorer")
	helpTexts.push("Clicking a directory, makes it the Current directory")
	helpTexts.push("Search is done in the tree with the Current directory as root")
	helpTexts.push("Clicking a thumbnail shows the high resolution image")
	helpTexts.push("High resolution images are draggable and zoomable")
	helpTexts.push("[Share] copies a URL to the clipboard")
	helpTexts.push("Search words are named A, B and C")
	helpTexts.push("Sort order: AB A B or ABC AB AC BC A B C")
	helpTexts.push("Contact: janchrister punkt nilsson alfakrull gmail punkt com")
</script>

<div>
	{#each helpTexts as helpText}
		<div style="width:475px;">
			&nbsp; • {helpText}
		</div>
		{/each}
		<div style="width:475px;">
			<img class="center" src="./qr.png" alt="QR" style="width:200px;">
		</div>
	</div>

<style>
.center {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 475px;
}
</style>
