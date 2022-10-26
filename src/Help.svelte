<script>
	const helpTexts = []
	helpTexts.push("Separate words with a space or an underscore (_)")
	helpTexts.push("Only the Current directory is searched")
	helpTexts.push("Search is case sensitive")
	helpTexts.push("Searching can start anywhere in a word")
	helpTexts.push("Search period like 2022-09-17, 2022-09, 2022 or 09-17")
	helpTexts.push("Search Tournament numbers like T10370")
	helpTexts.push("Search Member numbers like M585772")
	helpTexts.push("[None] unmarks images")
	helpTexts.push("[Download] zips marked images")
	helpTexts.push("[All] marks images")
	helpTexts.push("[Home] makes the Home directory the Current directory")
	helpTexts.push("The Current directory is shown in bold")
	helpTexts.push("Directories below it are in the Current directory")
	helpTexts.push("High resolution images are draggable and zoomable")
	helpTexts.push("[Share] copies a URL to the clipboard")
	helpTexts.push("Search words are named A, B and C")
	helpTexts.push("Sort order: ABC AB AC BC A B C")
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
