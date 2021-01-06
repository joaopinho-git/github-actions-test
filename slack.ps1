param(
    [string]  $ChannelName ,
    [string]  $Message ,
    [string]  $SenderName ='Release Team',
    [string]  $IconURL = 'http://icons.iconarchive.com/icons/xenatt/the-circle/512/App-Messages-icon.png',
    [string]  $MessageDetail = ''
	[string]  $FarfetchToken = ''
)

if(!$ChannelName.StartsWith('#'))
{
	$ChannelName = '#'+$ChannelName
}
   
$uri = 'https://slack.com/api/chat.postMessage'

$body = @{token = $FarfetchToken
	channel  = $ChannelName
	username = $SenderName
	parse    = 'full'
	icon_url = $IconURL
	text     = $Message + ' ' + $MessageDetail}

# Call the API
try 
{
    $result=Invoke-WebRequest -Uri $uri  -Method Post -Body $body -UseBasicParsing
    if($result.StatusCode -eq 200)
    {
        write-host "Message Sent to Slack"
    }else
    {
        Write-Error "Problems writing to Slack"
    }
}
catch 
{
    $ErrorActionPreference = "Continue" 	
	$errorDetail = $($_.Exception.Message)
    Write-Warning "======================================[SKIPPABLE ERROR] [ Unable to call the API:  $errorDetail ]======================================"
}